from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200)
    default_rate = models.IntegerField(default=0)
    total_time = models.IntegerField(default=0)
    recording_started_at = models.DateTimeField(null=True, blank=True)
    recording_stopped_at = models.DateTimeField(null=True, blank=True)
    is_recording = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', related_name='projects', on_delete=models.CASCADE, null=True)
    slug = models.SlugField(default='', null=False)

    def __str__(self):
        return self.name

class TimeEntry(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    duration = models.IntegerField(default=0)
    rate = models.IntegerField(default=0)

    def __str__(self):
        return self.project.name + " - " + str(self.start_time) + " - " + str(self.end_time)