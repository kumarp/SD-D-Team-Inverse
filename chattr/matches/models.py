from django.db import models
from django.contrib.auth.models import User
from chattr.jqchat.models import Room

#create this table
class RoomUsers(models.Model):
    room = models.ForeignKey(Room)
    user1 = models.ForeignKey(User, related_name = 'roomusers1_set')
    user2 = models.ForeignKey(User, null = True, blank=True, related_name = 'roomusers2_set')
    matchAll = models.BooleanField()
    expired = models.BooleanField()
    
    def __unicode__(self):
        return ' '.join([self.room.__unicode__(), self.user1.__unicode__(), (self.user2.__unicode__() if self.user2 else '')])
