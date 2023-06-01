from django.contrib import admin
from .models import Project, TimeEntry

# Register your models here.

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_time', 'is_recording', 'recording_started_at', 'recording_stopped_at')
    prepopulated_fields = {'slug': ("name",)}

admin.site.register(Project, ProjectAdmin)

class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('project', 'start_time', 'end_time', 'duration')

admin.site.register(TimeEntry, TimeEntryAdmin)