from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import GenericIPAddressField

# Create your models here.

class StudentUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile= models.CharField(max_length=15,null=True)
    gender=models.CharField(max_length=10,null=True)
    type= models.CharField(max_length=15,null=True)

    def __str__(self):
        return self.user.username
    

class Recruiter(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    mobile= models.CharField(max_length=15,null=True)
    gender=models.CharField(max_length=10,null=True)
    company=models.CharField(max_length=25,null=True)
    type= models.CharField(max_length=15,null=True)
    status=models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.user.username


class Job(models.Model):
    recruiter = models.ForeignKey(Recruiter,on_delete=models.CASCADE)
    start_date= models.DateField()
    end_date=models.DateField()
    title=models.CharField(max_length=100)
    salary= models.FloatField(max_length=20)
    description=models.CharField(max_length=500)
    experience=models.CharField(max_length=50)
    location=models.CharField(max_length=100)
    skills=models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Apply(models.Model):
    job=models.ForeignKey(Job,on_delete=models.CASCADE)
    student=models.ForeignKey(StudentUser,on_delete=models.CASCADE)
    resume=models.FileField(null=True)
    applydate=models.DateField()

    def __str__(self):
        return self.id