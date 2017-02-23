from django.contrib import admin
from .models import DataSource, Database, Tag, Publication
from .forms import publication_model_form_factory


class DataSourceAdmin(admin.ModelAdmin):
    list_display = ('short_notes',)
    search_fields = ('notes',)


class DatabaseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class PublicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_description', 'creator', 'created',
                    'modified', 'publishable',)
    search_fields = ('name', 'description', 'creator__username', 'server_path',
                     'responsibles__username', 'tags__name',)
    list_filter = ('publishable', 'created', 'modified', 'tags', 'creator',
                   'responsibles',)
    ordering = ('-created',)
    date_hierarchy = 'created'

    def get_form(self, request, obj=None, **kwargs):
        kwargs['form'] = publication_model_form_factory(request.user)
        return super(PublicationAdmin, self).get_form(request, obj, **kwargs)

    def get_fields(self, request, obj=None, **kwargs):
        fields = ('name', 'description', 'programming_language', 'data_sources',
                  ('update_value', 'update_type'), 'responsibles',
                  'databases', 'server_path', 'file_path', 'graph_path', 'publishable',
                  'created', 'modified', 'started', 'tags',)
        if request.user.is_superuser:
            fields = ('creator',) + fields
        return fields

    def get_actions(self, request):
        actions = super(PublicationAdmin, self).get_actions(request)
        if not request.user.is_superuser:
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if obj is not None and request.user == obj.creator:
            return True
        return False


admin.site.register(DataSource, DataSourceAdmin)
admin.site.register(Database, DatabaseAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Publication, PublicationAdmin)
