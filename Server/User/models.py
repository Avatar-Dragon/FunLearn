from django.db import models

# Create your models here.
class User(models.Model):
    """docstring for user"""
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    scores = models.IntegerField(default=0)
    maxContinuousCorrect = models.IntegerField(default=0)
    phone = models.CharField(max_length=11, default="")
    email = models.EmailField(default='')