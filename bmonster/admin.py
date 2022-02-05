from django.contrib import admin

from bmonster.models import Studio, Performer, Program, Schedule


class StudioModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'created_datetime', 'modified_datetime')
    readonly_fields = ('created_datetime', 'modified_datetime')


class PerformerModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_datetime', 'modified_datetime')
    readonly_fields = ('id', 'name', 'created_datetime', 'modified_datetime')


class ProgramModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'performer', 'name', 'created_datetime', 'modified_datetime')
    readonly_fields = ('id', 'performer', 'name', 'created_datetime', 'modified_datetime')


class ScheduleModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'studio', 'start_time', 'performer', 'program', 'created_datetime', 'modified_datetime')
    readonly_fields = ('id', 'studio', 'start_time', 'performer', 'program', 'created_datetime', 'modified_datetime')


admin.site.register(Studio, StudioModelAdmin)
admin.site.register(Performer, PerformerModelAdmin)
admin.site.register(Program, ProgramModelAdmin)
admin.site.register(Schedule, ScheduleModelAdmin)
