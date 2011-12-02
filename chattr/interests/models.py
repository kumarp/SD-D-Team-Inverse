from django.db import models
from django.contrib.auth.models import User

# Create Interest table
class Interest(models.Model):
    name = models.CharField(max_length=80)
    
    def __unicode__(self):
        return self.name

# Create User Interest relational table        
class UserInterestLink(models.Model):
    user = models.ForeignKey(User)
    interest = models.ForeignKey(Interest)

    def __unicode__(self):
        return self.interest.name
        