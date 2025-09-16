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


]