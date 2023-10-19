from django.db import models
from django.core import validators

class NewUser(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=16)
    password2 = models.CharField(max_length=16)
    email = models.EmailField(default=None,unique=True)
    
    
    def __str__(self):
        return self.name
    
class TodoModel(models.Model):
    email = models.EmailField(max_length=160,default=None,null=True)
    taskname = models.CharField(max_length=20)
    comments = models.TextField()
    status = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.taskname

