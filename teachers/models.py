from django.db import models

class Teacher(models.Model):
    teacher_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    email = models.EmailField()
    login_id = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
