from django.contrib import admin

from .models import Studio


class StudioModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'created_datetime', 'modified_datetime')
    readonly_fields = ('created_datetime', 'modified_datetime')


admin.site.register(Studio, StudioModelAdmin)
