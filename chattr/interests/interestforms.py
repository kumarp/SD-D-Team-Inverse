from django.db import models
from django import forms
from models import Interest, UserInterestLink
from django.contrib.auth.models import User

#form which creates a new interest and adds it to the user's interests
#generated from the Interest model (see models.py)
class NewInterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        
    def __init__(self, *args, **kwargs):
        super (NewInterestForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = ""

#form which adds an existing interest to the user's interests
#generated from the UserInterestLink model (see models.py)
class AddInterestForm(forms.ModelForm):
    class Meta:
        model = UserInterestLink
        fields = ('interest',)
        
    def __init__(self, user, *args, **kwargs):
        super (AddInterestForm, self).__init__(*args, **kwargs)
        self.fields['interest'].label = ""
        self.fields['interest'].empty_label = "--------------------------------"
        #limits interests in dropdown to those not in user's current interests
        #userinterests = UserInterestLink.objects.filter(user=user)
        #self.fields['interest'].queryset = Interest.objects.extra(where=['0=(SELECT COUNT(*) FROM interests_userinterestlink WHERE User = ' + str(user.id) + ' AND interests_userinterestlink = interest_id'])
        #self.fields['interest'].queryset = Interest.objects.extra(where=['0 = (SELECT COUNT(*) FROM interests_userinterestlink WHERE user_id = ' + str(user.id) + ' AND interest_id = interests_interest.id'])
        #self.fields['interest'].queryset = interests
        #userinterests = user.userinterestlink_set.all()
        #self.fields['interest'].queryset = Interest.objects.exclude(user=user)
        #self.fields['interest'].queryset = user.userinterestlink_set.all()
        
#form which removes an existing interest from the user's interests
#generated from the UserInterestLink model (see models.py)
class RemoveInterestForm(forms.Form):
    interest = forms.ModelChoiceField(UserInterestLink.objects.all())
        
    def __init__(self, user, *args, **kwargs):
        super (RemoveInterestForm, self).__init__(*args, **kwargs)
        #limits interests in dropdown to user's current interests
        self.fields['interest'].queryset = UserInterestLink.objects.filter(user__exact=user)
        self.fields['interest'].label = ""
        self.fields['interest'].empty_label = "--------------------------------"
