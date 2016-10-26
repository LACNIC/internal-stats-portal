from django import forms
from django.core.exceptions import ObjectDoesNotExist
from easy_select2 import apply_select2
from django.contrib.admin.widgets import FilteredSelectMultiple
from .models import Publication


def publication_model_form_factory(input_user):
    class PublicationModelForm(forms.ModelForm):

        def clean(self):
            cleaned_data = super(PublicationModelForm, self).clean()
            try:
                if not input_user.is_superuser and \
                                input_user != self.instance.creator:
                    raise forms.ValidationError(
                        'Solo puedes modificar publicaciones de las cuales'
                        ' seas el creador.', code='invalid')
            except ObjectDoesNotExist:
                # FK hasn't loaded yet.
                pass
            return cleaned_data

        def save(self, *args, **kwargs):
            obj = super(PublicationModelForm, self).save(*args, **kwargs)
            if obj.pk is None and not input_user.is_superuser:
                obj.creator = input_user
            obj.save()
            return obj

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
