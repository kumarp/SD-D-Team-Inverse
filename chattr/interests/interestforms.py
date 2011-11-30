from django.db import models
from django import forms
from models import Interest, UserInterestLink
from django.contrib.auth.models import User

class NewInterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        
    #def save(self, user, interest):
        #link = UserInterestLink(user=user, interest=interest)
        #return super(NewInterestForm, self).save()
        
class AddInterestForm(forms.ModelForm):
    class Meta:
        model = UserInterestLink
        fields = ('interest',)
        
    #def __init__(self, user, *args, **kwargs):
        #print "\n"
        #print user
        #print "\nscience"
        #self.user = user
        #super(AddInterestForm, self).__init__(*args, **kwargs)
        #print "\neveryday im sciencin\n"
        
    #def save(self):
        #self.user = User.objects.get(id=self.user.id)
        #return super(AddInterestForm, self).save()