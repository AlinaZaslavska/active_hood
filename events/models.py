from django.db import models
from django.contrib.auth.models import User
from locations.models import City
from users.models import Activity

class Event(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    description = models.TextField(default="Describe your event")
    date = models.DateField()
    time = models.TimeField(null=True)
    location = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    participants = models.ManyToManyField(User, blank=True, related_name='participating_events')
  
    def __str__(self):
        return f"{self.activity}, {self.date}"
    