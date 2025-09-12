from django.db import models
from django.contrib.auth.models import User

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
    cpr=models.IntegerField()
    occupation=models.CharField(max_length=120)
    email=models.EmailField(max_length=100)
    department=models.CharField(max_length=2, choices=DEPARTMENTS,default=DEPARTMENTS[0][0])
    role=models.CharField(max_length=1, choices=ROLES,default=ROLES[1][0])
    

    def __str__(self):
        return f"{self.user.username} {self.get_role_display()} {self.get_department_display()}"