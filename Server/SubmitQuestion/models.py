from django.db import models
from User.models import User

# Create your models here.
class SubmitMultipleQuestion(models.Model):
    category = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=50)
    string_question = models.TextField()
    correct_answer = models.CharField(max_length=200)
    incorrect_answersA = models.CharField(max_length=200)
    incorrect_answersB = models.CharField(max_length=200)
    incorrect_answersC = models.CharField(max_length=200)
    permit = models.CharField(max_length=50, default="wait")
    user = models.ForeignKey(User)

class SubmitBooleanQuestion(models.Model):
    category = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=50)
    string_question = models.TextField()
    correct_answer = models.CharField(max_length=200)
    incorrect_answers = models.CharField(max_length=200)
    permit = models.CharField(max_length=50, default="wait")
    user = models.ForeignKey(User)