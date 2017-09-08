from django.contrib import admin
from models import Redirect, Visit


class VisitAdmin(admin.ModelAdmin):
    list_display = ('url', 'date', 'publication',)

    def get_readonly_fields(self, request, obj=None):
        return ('url', 'date', 'publication',)


admin.site.register(Redirect)
admin.site.register(Visit, VisitAdmin)
