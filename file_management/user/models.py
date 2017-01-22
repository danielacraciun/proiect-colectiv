from django.contrib.auth.models import User
from django.db import models
from django.db.models import signals
from django.utils.timezone import now

from documents.models import FluxInstance
from user.constants import UserRoles


class Notification(models.Model):
    from_user = models.ForeignKey(User, related_name='sent_notifications', null=True, blank=True)
    to_user = models.ForeignKey(User, related_name='received_notifications', null=True, blank=True)
    flux = models.ForeignKey(FluxInstance, related_name='messages', null=True, blank=True)
    message = models.CharField(max_length=300, null=False, blank=False, default="")
    date = models.DateField(null=True, blank=True, default=now)

    def __str__(self):
        return "from: {}, to: {}, message: {}".format(self.from_user, self.to_user, self.message)


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
