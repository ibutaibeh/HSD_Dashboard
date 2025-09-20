from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import AdminOnlyMixin
from .forms import UpdateProfileForm
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import SurveyOperations, SurveyTypes, Agencies, SurveyAttributes

# Create your views here.

def home(request):
    return render(request,'home.html')

@login_required
def signup(request):
    if request.user.profile.role == 'A':
        error_message= ''
        if request.method == 'POST':
            form=UserCreationForm(request.POST)
            if form.is_valid():
                user= form.save()
                # login(request,user)
                return redirect('signup')
            else:
                error_message='Invalid sign up - try again later'
        form = UserCreationForm()
        context = {'form':form, 'error_message':error_message}
        return render(request,'registration/signup.html',context)
    else:
        return redirect('/')

@login_required
def profile(request):
    if request.method == 'POST':
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('/profile')
    else:
        profile_form = UpdateProfileForm(instance=request.user.profile)
    return render(request,'profile.html',{'profile_form':profile_form})

class ChangePasswordView(SuccessMessageMixin,PasswordChangeView):
    template_name= 'change_password.html'
    success_message= 'Successfully Changed Your Password'
    success_url= reverse_lazy('profile')

#CBVs for Survey Operations 
class SurveyOperationsList(LoginRequiredMixin,ListView):
    model=SurveyOperations

class SurveyOperationsDetail(LoginRequiredMixin,DetailView):
    model=SurveyOperations

class SurveyOperationsCreate(LoginRequiredMixin,CreateView):
    model=SurveyOperations
    fields= '__all__'

class SurveyOperationsUpdate(LoginRequiredMixin,UpdateView):
    model=SurveyOperations
    fields='__all__'

class SurveyOperationsDelete(LoginRequiredMixin,DeleteView):
    model=SurveyOperations
    success_url='/survey_operations/'



#CBVs for Survey Types
class SurveyTypesList(LoginRequiredMixin,AdminOnlyMixin,ListView):
    model=SurveyTypes

class SurveyTypesDetail(LoginRequiredMixin,AdminOnlyMixin,DetailView):
    model=SurveyTypes

class SurveyTypesCreate(LoginRequiredMixin,AdminOnlyMixin,CreateView):
    model=SurveyTypes
    fields= '__all__'

class SurveyTypesUpdate(LoginRequiredMixin,AdminOnlyMixin,UpdateView):
    model=SurveyTypes
    fields='__all__'

class SurveyTypesDelete(LoginRequiredMixin,AdminOnlyMixin,DeleteView):
    model=SurveyTypes
    success_url='/survey_types/'


#CBVs for Agencies 
class AgenciesList(LoginRequiredMixin,AdminOnlyMixin,ListView):
    model=Agencies

class AgenciesDetail(LoginRequiredMixin,AdminOnlyMixin,DetailView):
    model=Agencies

class AgenciesCreate(LoginRequiredMixin,AdminOnlyMixin,CreateView):
    model=Agencies
    fields= '__all__'

class AgenciesUpdate(LoginRequiredMixin,AdminOnlyMixin,UpdateView):
    model=Agencies
    fields='__all__'

class AgenciesDelete(LoginRequiredMixin,AdminOnlyMixin,DeleteView):
    model=Agencies
    success_url='/agencies/'

#CBVs for Survey Attributes
class SurveyAttributesList(LoginRequiredMixin,AdminOnlyMixin,ListView):
    model=SurveyAttributes
    ordering= ['survey_type__name','name']


class SurveyAttributesDetail(LoginRequiredMixin,AdminOnlyMixin,DetailView):
    model=SurveyAttributes

class SurveyAttributesCreate(LoginRequiredMixin,AdminOnlyMixin,CreateView):
    model=SurveyAttributes
    fields= '__all__'

class SurveyAttributesUpdate(LoginRequiredMixin,AdminOnlyMixin,UpdateView):
    model=SurveyAttributes
    fields='__all__'

class SurveyAttributesDelete(LoginRequiredMixin,AdminOnlyMixin,DeleteView):
    model=SurveyAttributes
    success_url='/survey_attributes/'
