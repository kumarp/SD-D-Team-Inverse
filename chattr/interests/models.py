from django.db import models
from django.contrib.auth.models import User

# create these tables
class Interest(models.Model):
    name = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.name
        
class UserInterestLink(models.Model):
    user = models.ForeignKey(User)
    interest = models.ForeignKey(Interest)

    def __unicode__(self):
        return self.interest.name
        