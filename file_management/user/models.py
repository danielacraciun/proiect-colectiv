from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals

from user.constants import UserRoles


class UserProfile(models.Model):

    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name='profile')
    role = models.IntegerField(default=1, choices=UserRoles.USER_GROUPS_CHOICES)

    def __str__(self):
        return self.user.username


def create_user_profile(sender, instance, signal, created, **kwargs):
    if created:
        user_profile, _ = UserProfile.objects.get_or_create(user=instance)
        user_profile.save()

signals.post_save.connect(create_user_profile, User)
