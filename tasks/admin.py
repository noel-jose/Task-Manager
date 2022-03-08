from django.contrib import admin

# Register your models here.
from tasks.models import Task
from tasks.models import TaskHistory
from tasks.models import Profile

admin.sites.site.register(Task)
admin.sites.site.register(TaskHistory)
admin.sites.site.register(Profile)
