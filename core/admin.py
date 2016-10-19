from django.contrib import admin
from easy_select2 import select2_modelform
from .models import DataSource, Database, Tag, Publication


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
    search_fields = ('name', 'description', 'creator__username', 'server_path',)
    list_filter = ('publishable', 'created', 'modified',)
    filter_horizontal = ('data_sources', 'responsibles', 'databases',)
    ordering = ('-created',)
    form = select2_modelform(Publication)


admin.site.register(DataSource, DataSourceAdmin)
admin.site.register(Database, DatabaseAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Publication, PublicationAdmin)
