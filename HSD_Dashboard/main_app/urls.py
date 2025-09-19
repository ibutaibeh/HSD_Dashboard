from django.contrib import admin
from django.urls import path
from . import views


urlpatterns=[
    path('',views.home,name='home'),
    #user accounts and profile
    path('accounts/signup/',views.signup, name='signup'),
    path('profile/',views.profile,name='profile'),
    path('profile/change_password/',views.ChangePasswordView.as_view(), name='change_password'),
    #Survey Operation DashBoard 
    path('survey_operations/',views.SurveyOperationsList.as_view(), name='survey_index'),
    path('survey_operations/<int:pk>/',views.SurveyOperationsDetail.as_view(),name='survey_detail'),
    path('survey_operations/create/',views.SurveyOperationsCreate.as_view(),name='survey_create'),
    path('survey_operations/<int:pk>/update/',views.SurveyOperationsUpdate.as_view(),name='survey_update'),
    path('survey_operations/<int:pk>/delete/',views.SurveyOperationsDelete.as_view(),name='survey_delete'),
    #Survey Types DashBoard
    path('survey_types/',views.SurveyTypesList.as_view(), name='type_index'),
    path('survey_types/<int:pk>/',views.SurveyTypesDetail.as_view(),name='type_detail'),
    path('survey_types/create/',views.SurveyTypesCreate.as_view(),name='type_create'),
    path('survey_types/<int:pk>/update/',views.SurveyTypesUpdate.as_view(),name='type_update'),
    path('survey_types/<int:pk>/delete/',views.SurveyTypesDelete.as_view(),name='type_delete'),
    #Agencies Dashboard 
    path('agencies/',views.AgenciesList.as_view(), name='agency_index'),
    path('agencies/<int:pk>/',views.AgenciesDetail.as_view(),name='agency_detail'),
    path('agencies/create/',views.AgenciesCreate.as_view(),name='agency_create'),
    path('agencies/<int:pk>/update/',views.AgenciesUpdate.as_view(),name='agency_update'),
    path('agencies/<int:pk>/delete/',views.AgenciesDelete.as_view(),name='agency_delete'),
    #survey_attributes Dashboard 
    path('survey_attributes/',views.SurveyAttributesList.as_view(), name='attribute_index'),
    path('survey_attributes/<int:pk>/',views.SurveyAttributesDetail.as_view(),name='attribute_detail'),
    path('survey_attributes/create/',views.SurveyAttributesCreate.as_view(),name='attribute_create'),
    path('survey_attributes/<int:pk>/update/',views.SurveyAttributesUpdate.as_view(),name='attribute_update'),
    path('survey_attributes/<int:pk>/delete/',views.SurveyAttributesDelete.as_view(),name='attribute_delete'),


]