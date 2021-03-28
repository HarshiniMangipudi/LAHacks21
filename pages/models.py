from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
from django.utils import timezone
from django.urls import reverse 


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fb_email = models.EmailField()
    fb_password = models.CharField(max_length=100)
    fb_cookie_c_user = models.CharField(max_length=50, blank=True)
    fb_cookie_xs = models.CharField(max_length=200, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Task(models.Model):
    task_name = models.CharField(max_length=300, blank=False)
    body = models.TextField(verbose_name="Description")
    date_added = models.DateTimeField(default=timezone.now, verbose_name="Date Added")
    date_due = models.DateTimeField(default=(datetime.utcnow() + timedelta(days=2)), verbose_name="Date Due")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Sunday = models.BooleanField(default=True)
    Monday = models.BooleanField(default=True)
    Tuesday = models.BooleanField(default=True)
    Wednesday = models.BooleanField(default=True)
    Thursday = models.BooleanField(default=True)
    Friday = models.BooleanField(default=True)
    Saturday = models.BooleanField(default=True)
    time_of_day = models.TimeField(default=timezone.now)
    friend_fb_id = models.CharField(max_length=300, blank=False, default='enter user id')

    def __str__(self):
        return self.task_name