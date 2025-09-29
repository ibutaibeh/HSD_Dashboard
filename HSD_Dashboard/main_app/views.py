from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import AdminOnlyMixin
from .forms import DataImportForm, UpdateProfileForm
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import SurveyOperations, SurveyTypes, Agencies, SurveyAttributes, DataImport
from django.contrib import messages
import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db.models.functions import Transform


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
    def get_context_data(self, **kwargs):
        ctx =super().get_context_data(**kwargs)
        if self.object.location:
            obj = (
                SurveyOperations.objects
                .filter(pk=self.object.pk)
                .annotate(geom4326=Transform("location", 4326))
                .first()
            )
            ctx["location4326"] = obj.geom4326.geojson if obj and obj.geom4326 else None

        return ctx

class SurveyOperationsCreate(LoginRequiredMixin,CreateView):
    model=SurveyOperations
    fields= '__all__'

    def form_valid(self, form):
        geom_str = self.request.POST.get("location")
        if geom_str:
            geom = GEOSGeometry(geom_str,srid=4326)
            geom.transform(32639)
            form.instance.location=geom
        return super().form_valid(form)


class SurveyOperationsUpdate(LoginRequiredMixin,UpdateView):
    model=SurveyOperations
    fields='__all__'
    def form_valid(self, form):
        geom_str = self.request.POST.get("location")
        if geom_str:
            geom = GEOSGeometry(geom_str,srid=4326)
            geom.transform(32639)
            form.instance.location=geom
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        ctx =super().get_context_data(**kwargs)
        if self.object.location:
            obj = (
                SurveyOperations.objects
                .filter(pk=self.object.pk)
                .annotate(geom4326=Transform("location", 4326))
                .first()
            )
            ctx["location4326"] = obj.geom4326.geojson if obj and obj.geom4326 else None

        return ctx

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

#CBVs for Data import - Survey Operations attributes
class DataImportList(LoginRequiredMixin,ListView):
    model=DataImport

class DataImportDetail(LoginRequiredMixin,DetailView):
    model=DataImport

class DataImportDelete(LoginRequiredMixin,DeleteView):
    model=DataImport
    success_url='/dataimport/'

@login_required
def dataimport_entry(request, pk):
    #getting the Survey with pk
    survey= SurveyOperations.objects.get(pk=pk)
    #set up the formset without extra empty row at the end
    DataImportFormSet= modelformset_factory(DataImport,form= DataImportForm, extra=0)

    #if Dataimport exist,
    dataimports= DataImport.objects.filter(survey_operation=survey)

    # if it doesnt exist: create the form
    if not dataimports.exists():
        objs=[]
        attributes= SurveyAttributes.objects.filter(survey_type= survey.survey_type)
        for attribute in attributes:
            objs.append(DataImport(survey_operation=survey, survey_attribute=attribute))
        DataImport.objects.bulk_create(objs)
        dataimports=DataImport.objects.filter(survey_operation=survey)

    if request.method == "POST":
        formset= DataImportFormSet(request.POST, queryset=dataimports)
        if formset.is_valid():
            formset.save()
            #messages.success(request,"Data imported successfully!")
            return redirect("survey_detail",pk=survey.pk)
    else:
        formset= DataImportFormSet(queryset=dataimports)

    return render(request, "main_app/dataimport_formset.html",{"formset":formset, "survey":survey})

