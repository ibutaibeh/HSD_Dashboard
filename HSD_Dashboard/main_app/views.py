from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UpdateProfileForm
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy

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