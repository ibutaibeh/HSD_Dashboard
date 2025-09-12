from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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
                login(request,user)
                return redirect('home')
            else:
                error_message='Invalid sign up - try again later'
        form = UserCreationForm()
        context = {'form':form, 'error_message':error_message}
        return render(request,'registration/signup.html',context)
    else:
        return redirect('/')

@login_required
def profile(request):
    return render(request,'profile.html')

