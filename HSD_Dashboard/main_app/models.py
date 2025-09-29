#from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse

# Create your models here.
#Agencies Model
class Agencies(models.Model):
    TYPES= (
        ('H','HSD'),
        ('G','Government'),
        ('P','Private'),
        ('M','Military'),
    )
    name= models.CharField(max_length=120, unique=True)
    type= models.CharField(max_length=1, choices=TYPES)
    remarks= models.CharField(max_length=250, null=True, blank=True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('agency_detail', kwargs={'pk':self.id})
#-----------------------------------------------------------------------------
#Survey Type Model
class SurveyTypes(models.Model):
    code= models.CharField(max_length=10, unique=True)
    name= models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('type_detail', kwargs={'pk':self.id})  
#-----------------------------------------------------------------------------
# Survey Attributes
class SurveyAttributes(models.Model):
    survey_type= models.ForeignKey(SurveyTypes,on_delete=models.DO_NOTHING)
    name= models.CharField(max_length=100)
    unit= models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.survey_type.code} - {self.name}"
    def get_absolute_url(self):
        return reverse('attribute_detail', kwargs={'pk':self.id})
#-----------------------------------------------------------------------------
class Profile(models.Model):
    DEPARTMENTS=(
    ('MO','Marine Operations'),
    ('CP','Charts Production'),
    )
    ROLES=(
        ('A','admin'),
        ('B','viewer'),
    )
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    avatar= models.ImageField(upload_to='main_app/static/uploads',default='main_app/static/images/DefaultAvatar.jpg')
    cpr=models.IntegerField(null=True)
    occupation=models.CharField(max_length=120, null=True)
    email=models.EmailField(max_length=100, null=True)
    department=models.CharField(max_length=2, choices=DEPARTMENTS,default=DEPARTMENTS[0][0])
    role=models.CharField(max_length=1, choices=ROLES,default=ROLES[1][0]) 

    def __str__(self):
        return f"{self.user.username} {self.get_role_display()} {self.get_department_display()}"
    def save(self, *args, **kwargs):
        super().save()
        img= Image.open(self.avatar.path)
        if img.height > 100 or img.width >100:
            new_img= (250,250)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
#-----------------------------------------------------------------------------
#Survey Opreations Model
class SurveyOperations(models.Model):
    STATUSES=(
        ('P','planned'),
        ('O','ongoing'),
        ('C','completed'),
        ('X','cancelled'),
    )
    survey_name= models.CharField(max_length=100)
    start_date= models.DateField()
    end_date= models.DateField()
    survey_type= models.ForeignKey(SurveyTypes,on_delete=models.CASCADE)
    status= models.CharField(max_length=1,choices=STATUSES)
    location= models.PolygonField(srid=32639) #srid=32639 issue store and retrieve
    surveyor= models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="as_surveyor")
    data_processor= models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="as_data_processor")
    qc_processor= models.ForeignKey(User,null=True, on_delete=models.SET_NULL,related_name="as_qc_processor")
    agency= models.ForeignKey(Agencies,on_delete=models.CASCADE)

    def __str__(self):
        return self.survey_name
    
    def get_absolute_url(self):
        return reverse('survey_detail', kwargs={'pk':self.id})
#-----------------------------------------------------------------------------    

#Data Import - Survey Attributes values 
class DataImport(models.Model):
    survey_operation= models.ForeignKey(SurveyOperations,on_delete=models.CASCADE)
    survey_attribute= models.ForeignKey(SurveyAttributes,on_delete=models.CASCADE)
    value = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.survey_operation.survey_name} - {self.survey_attribute.name}: {self.value} {self.survey_attribute.unit or ''}"






