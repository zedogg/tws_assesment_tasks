from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


class User(AbstractUser):
    email=models.EmailField(unique=True)
    verified_at = models.CharField(max_length=200,default='True')
    role =models.CharField(max_length=200,default='user')
    status = models.CharField(max_length=20, default='1')
    updated_at = models.CharField(max_length=200,default=datetime.utcnow())
    created_at = models.CharField(max_length=200,default=datetime.utcnow())
    remember_token=models.CharField(max_length=200,null=True)


class Tasks(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.CharField(max_length=200)
    created_at = models.CharField(max_length=200)
    status = models.CharField(max_length=100,default= '1')

class AssignTasks(models.Model):
    user_id = models.ForeignKey('core.User',on_delete=models.CASCADE,db_column='user_id')
    task_id = models.ForeignKey('core.Tasks',on_delete=models.CASCADE,db_column='task_id')
    status = models.CharField(max_length=100,default='1')

