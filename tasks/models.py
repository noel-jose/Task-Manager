from django.db import models

from django.conf import settings

User = settings.AUTH_USER_MODEL

from django.utils import timezone

from datetime import datetime

import pytz

STATUS_CHOICES = (
    ("PENDING", "PENDING"),
    ("IN_PROGRESS", "INPROGRESS"),
    ("COMPLETED", "COMPLETED"),
    ("CANCELLED", "CANCELLED"),
)

TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    priority = models.IntegerField(null=True)
    created_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class TaskHistory(models.Model):
    previous_status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0]
    )
    current_status = models.CharField(
        max_length=100, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0]
    )
    change_date = models.DateTimeField(auto_now=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    alert_time = models.DateTimeField(null=True, blank=True, default=timezone.now())
    utc_time = models.TimeField(null=True)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default="UTC")
    next_update = models.DateTimeField(null=True)

    # def __str__(self):
    #     return self.user.username
