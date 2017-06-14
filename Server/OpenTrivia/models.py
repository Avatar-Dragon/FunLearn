from django.db import models

# Create your models here.
class multipleQuestion(models.Model):
    category = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=50)
    string_question = models.TextField()
    correct_answer = models.CharField(max_length=200)
    incorrect_answersA = models.CharField(max_length=200)
    incorrect_answersB = models.CharField(max_length=200)
    incorrect_answersC = models.CharField(max_length=200)

class booleanQuestion(models.Model):
    category = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=50)
    string_question = models.TextField()
    correct_answer = models.CharField(max_length=200)
    incorrect_answers = models.CharField(max_length=200)