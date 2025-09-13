from django.db import models
from django.contrib.auth.models import User
from PIL import Image

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