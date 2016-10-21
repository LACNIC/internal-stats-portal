from __future__ import unicode_literals
from django.conf import settings
from django.db.models import Model, TextField, OneToOneField, CASCADE
from django.db.models.signals import post_save


class UserProfile(Model):
    user = OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    comments = TextField('comentarios', blank=True, null=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = 'user profile'
        verbose_name_plural = 'user profiles'


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)
