from __future__ import unicode_literals
from django.conf import settings
from django.db.models import Model, TextField, OneToOneField, CASCADE


class UserProfile(Model):
    user = OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    comments = TextField('comentarios', blank=True, null=True)

    def __unicode__(self):
        return self.user.username

    class Meta:
        verbose_name = 'user profile'
        verbose_name_plural = 'user profiles'
