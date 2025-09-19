from django.contrib import admin
from .models import Profile, SurveyOperations,SurveyTypes, Agencies,SurveyAttributes,SurveyOperationsAttributes
# Register your models here.

admin.site.register(Profile)
admin.site.register(SurveyOperations)
admin.site.register(SurveyTypes)
admin.site.register(Agencies)
admin.site.register(SurveyAttributes)
admin.site.register(SurveyOperationsAttributes)
