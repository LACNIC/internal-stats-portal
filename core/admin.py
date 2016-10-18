from django.contrib import admin
from .models import Responsible, DataSource, Database, Publication


class ResponsibleAdmin(admin.ModelAdmin):
    list_display = ('responsible_username', 'responsible_full_name',
                    'responsible_email', 'comments',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name',
                     'user__email', 'comments',)

    def responsible_username(self, obj):
        return obj.user.username

    responsible_username.short_description = 'nombre de usuario'

    def responsible_full_name(self, obj):
        return obj.user.get_full_name()

    responsible_full_name.short_description = 'responsable'

    def responsible_email(self, obj):
        return obj.user.email

    responsible_email.short_description = 'email'


class DataSourceAdmin(admin.ModelAdmin):
    list_display = ('short_notes',)
    search_fields = ('notes',)


class DatabaseAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class PublicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_description', 'creator', 'created',
                    'last_modified', 'publishable',)
    search_fields = ('name', 'description', 'creator__username', 'server_path',)
    list_filter = ('publishable', 'created', 'last_modified',)
    filter_horizontal = ('data_sources', 'responsibles', 'databases',)
    ordering = ('-created',)


admin.site.register(Responsible, ResponsibleAdmin)
admin.site.register(DataSource, DataSourceAdmin)
admin.site.register(Database, DatabaseAdmin)
admin.site.register(Publication, PublicationAdmin)
