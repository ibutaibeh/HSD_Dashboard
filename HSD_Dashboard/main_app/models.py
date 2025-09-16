#from django.db import models
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse

# Create your models here.

# user profile model -one to one relationship with User
DEPARTMENTS=(
    ('MO','Marine Operations'),
    ('CP','Charts Production'),
)
ROLES=(
    ('A','admin'),
    ('B','viewer'),
)

class Profile(models.Model):
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


#Survey Opreations Model
class SurveyOperations(models.Model):
    STATUSES=(
        ('P','planned'),
        ('O','ongoing'),
        ('C','completed'),
        ('X','cancelled'),
    )
    SURVEYTYPES=(
        ('SBS','single-beam Survey'),
        ('MBS','multi-beam Survey'),
        ('SBP','sub-bottom Profiler Survey'),
    )
    survey_name= models.CharField(max_length=100)
    start_date= models.DateField()
    end_date= models.DateField()
    survey_type= models.CharField(max_length=3, choices=SURVEYTYPES, default=SURVEYTYPES[0][0])
    status= models.CharField(max_length=1,choices=STATUSES, default=STATUSES[2][0])
    location= models.PolygonField(srid=32639)
    surveyor= models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="as_surveyor")
    data_processor= models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="as_data_processor")
    qc_processor= models.ForeignKey(User,null=True, on_delete=models.SET_NULL,related_name="as_qc_processor")

    def __str__(self):
        return self.survey_name
    
    def get_absolute_url(self):
        return reverse('survey_detail', kwargs={'pk':self.id})





