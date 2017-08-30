from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from core.models import Publication


class Redirect(models.Model):
    """
        class to persist all redirects served
    """
    redirect_from = models.URLField()
    redirect_to = models.URLField()
    date = models.DateTimeField(default=datetime.now)

    publication = models.ForeignKey(Publication, default=1)
