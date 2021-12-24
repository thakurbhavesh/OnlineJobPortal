from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class StudentUser(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=15,null=True)
    image=models.FileField(null=True)
    gender=models.CharField(max_length=10,null=True)
    type=models.CharField(max_length=15,null=True)
    def __str__(self):
        return self.user.username

class Recruiter(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=15,null=True)
    image=models.FileField(null=True)
    gender=models.CharField(max_length=10,null=True)
    company=models.CharField(max_length=100,null=True)
    type=models.CharField(max_length=15,null=True)
    status=models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.user.username

class Job(models.Model):

    start_date=models.DateField()
    end_date = models.DateField()
    title=models.CharField(max_length=100)
    salary= models.CharField(max_length=100)
    image=models.FileField(null=True)
    description= models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    skills = models.CharField(max_length=100)
    creationdate = models.DateField()
    def __str__(self):
        return self.title

class Placed(models.Model):
    image=image=models.FileField(null=True)
    title = models.CharField(max_length=100)
