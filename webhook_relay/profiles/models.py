from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.ForeignKey('auth.User')


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    if kwargs['created'] is True:
        UserProfile.objects.create(user_id=kwargs['instance'].id)
