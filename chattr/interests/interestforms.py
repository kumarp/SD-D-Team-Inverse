from django.db import models
from django import forms
from models import Interest, UserInterestLink
from django.contrib.auth.models import User

# Form which creates a new interest and adds it to the user's interests
# generated from the Interest model (see models.py)
class NewInterestForm(forms.ModelForm):
    class Meta:
        model = Interest
        
    def __init__(self, *args, **kwargs):
        super (NewInterestForm, self).__init__(*args, **kwargs)
        self.fields['name'].label = ""

# Form which adds an existing interest to the user's interests
# generated from the UserInterestLink model (see models.py)
class AddInterestForm(forms.ModelForm):
    class Meta:
        model = UserInterestLink
        fields = ('interest',)
        
    def __init__(self, user, *args, **kwargs):
        super (AddInterestForm, self).__init__(*args, **kwargs)
        self.fields['interest'].label = ""
        self.fields['interest'].empty_label = "--------------------------------"
        
# Form which removes an existing interest from the user's interests
# generated from the UserInterestLink model (see models.py)
class RemoveInterestForm(forms.Form):
    interest = forms.ModelChoiceField(UserInterestLink.objects.all())
        
    def __init__(self, user, *args, **kwargs):
        super (RemoveInterestForm, self).__init__(*args, **kwargs)
        # Limits interests in dropdown to user's current interests
        self.fields['interest'].queryset = UserInterestLink.objects.filter(user__exact=user)
        self.fields['interest'].label = ""
        self.fields['interest'].empty_label = "--------------------------------"
