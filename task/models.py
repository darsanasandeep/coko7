from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class UserProfile(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    address = models.CharField(max_length=20)
    city = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    DOB = models.DateField()
    profile = models.ImageField(upload_to='profile',null=True)


class UserTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_name = models.CharField(max_length=20)
    start_date = models.DateField()
    due_date = models.DateField()
    discrp = models.CharField(max_length=100)
    status = models.CharField(max_length=10)

