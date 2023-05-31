from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=200)
    total_time = models.IntegerField(default=0)
    recording_started_at = models.DateTimeField(null=True, blank=True)
    recording_stopped_at = models.DateTimeField(null=True, blank=True)
    is_recording = models.BooleanField(default=False)
    slug = models.SlugField(default='', null=False)

    def __str__(self):
        return self.name

    