from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.safestring import mark_safe
from django.conf import settings

# create this table
class UserRating(models.Model):
    user = models.ForeignKey(User)
    numRatings = models.IntegerField()
    totalRating = models.IntegerField()
    avgRating = models.FloatField()