from .models import Task, TaskHistory, Profile
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from task_manager.users.models import User


@receiver(pre_save, sender=Task)
def create_taskhistory(sender, instance, update_fields, **kwargs):
    # if Task.objects.filter(id=instance.id).exists():
    #     prev_status = Task.objects.filter(id=instance.id).values_list("status")
    #     curr_status = instance.status
    #     if prev_status != curr_status:
    #         history = TaskHistory(
    #             previous_status=prev_status, current_status=curr_status, task=instance
    #         )
    #         history.save()
    #         print(f"Successfully created a history for the task {instance.title}")

    if instance.id is None:
        pass
    else:
        prev_status = Task.objects.get(id=instance.id).status
        curr_status = instance.status
        if curr_status != prev_status:
            history = TaskHistory(
                previous_status=prev_status, current_status=curr_status, task=instance
            )
            history.save()
            print(
                f"Successfully created a new history for the change {prev_status} --> {curr_status}"
            )


# creating a profile instance when we create a user
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        print(f"Creating a Profile instance for user { instance.username }")
        user = instance
        profile = Profile(user=user)
        profile.save()
        print(f"Created a Profile for { instance.username }")
    else:
        pass


# # sending a request to add the celery task to the worker after being saved
# @receiver(post_save,sender=Profile)
# def create_task(sender,instance,created,**kwargs):

#     print(f"Updated the date of the profile { instance }")
#     time = str(instance.alert_time)
#     hours = time[0:2]
#     minutes = time[3:5]
#     setReminder(minutes,hours,instance)
#     print("Successfully completed the create_task_reminder")
