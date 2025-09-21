from django import forms
from django.contrib.auth.models import User
from .models import Profile,DataImport


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =["avatar", "cpr", "occupation", "email", "department"]


class DataImportForm(forms.ModelForm):
    class Meta:
        model = DataImport
        fields= ["value"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.survey_attribute:
            self.fields["value"].label = self.instance.survey_attribute.name



