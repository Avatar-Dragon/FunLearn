from django.db import models

# Create your models here.
class MathQuestion(models.Model):
    questionType = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=50)
    string_question = models.TextField()
    string_answer = models.CharField(max_length=200)
    problem_image_url = models.URLField()
    solution_image_url = models.URLField()
