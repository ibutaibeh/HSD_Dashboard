from django import forms
from django.contrib.auth.models import User
from .models import Profile, SurveyOperations


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =["avatar", "cpr", "occupation", "email", "department"]



