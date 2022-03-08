from rest_framework.serializers import ModelSerializer
from .models import Task, TaskHistory

from task_manager.users.models import User

# from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]


class TaskSerializer(ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ["title", "description", "priority", "completed", "status", "user"]


class TaskHistorySerializer(ModelSerializer):
    task = TaskSerializer(
        read_only=True,
    )

    class Meta:
        model = TaskHistory
        fields = ["previous_status", "current_status", "change_date", "task"]
