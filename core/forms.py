from django import forms
from django.core.exceptions import ObjectDoesNotExist
from easy_select2 import apply_select2
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Publication
from django.core.validators import URLValidator
from datetime import datetime

from requests import head as http_head


def publication_model_form_factory(input_user):
    class PublicationModelForm(forms.ModelForm):

        def clean(self):
            cleaned_data = super(PublicationModelForm, self).clean()
            errors = dict()

            try:
                if not input_user.is_superuser and \
                                input_user != self.instance.creator:
                    raise forms.ValidationError(
                        'Solo puedes modificar publicaciones de las cuales'
                        ' seas el creador.', code='invalid')
                    #
                dict__ = self.instance._meta.__dict__
                fields_ = dict__['_forward_fields_map']
                if not (cleaned_data['file_path'] or cleaned_data['graph_path']):

                    message = "Es necesario completar '%s' o '%s' (al menos uno de los dos)" % (
                        fields_['file_path'].verbose_name,
                        fields_['graph_path'].verbose_name
                    )
                    errors['file_path'] = message
                    errors['graph_path'] = message
                    raise forms.ValidationError(message=errors)
                else:
                    # At least one of them...

                    urls = {
                        'file_path': cleaned_data['file_path'],
                        'graph_path': cleaned_data['graph_path']
                    }
                    for k, url in urls.iteritems():
                        if url:
                            try:
                                URLValidator(url)
                                response_status_code = Publication.head_remote(
                                    url
                                ).status_code  # HEADs either via FTP (FTP SIZE command) or HTTP (HTTP HEAD) http_head(url=url).status_code
                                if response_status_code != 200:
                                    errors[k] = 'La ruta indicada no es accesible (Return Status != 200)'
                            except Exception as e:
                                errors[k] = e.message
                    raise forms.ValidationError(message=errors)

            except ObjectDoesNotExist:
                # FK hasn't loaded yet.
                pass
            return cleaned_data

        def save(self, *args, **kwargs):

            if self.has_changed():
                self.instance.modified = datetime.now()

            if self.instance.pk is None and not input_user.is_superuser:
                self.instance.creator = input_user
            return super(PublicationModelForm, self).save(*args, **kwargs)

        class Meta:
            model = Publication
            exclude = ()
            if not input_user.is_superuser:
                exclude = ('creator',)
            widgets = {
                'creator': apply_select2(forms.Select),
                'programming_language': apply_select2(forms.Select),
                'update_type': apply_select2(forms.Select),
                'tags': apply_select2(forms.SelectMultiple),
                'data_sources': FilteredSelectMultiple(
                    verbose_name="Fuentes de datos",
                    is_stacked=False, ),
                'responsibles': FilteredSelectMultiple(
                    verbose_name="Responsables",
                    is_stacked=False, ),
                'databases': FilteredSelectMultiple(
                    verbose_name="Bases de datos",
                    is_stacked=False, ),

            }

    return PublicationModelForm
