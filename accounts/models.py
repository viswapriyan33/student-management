from django.contrib.auth.models import AbstractUser
from django.db import models

# class User(AbstractUser):
#     ROLE_CHOICES = (
#         ('admin', 'Admin'),
#         ('teacher', 'Teacher'),
#         ('student', 'Student'),
#     )
#     role = models.CharField(max_length=10, choices=ROLE_CHOICES)

class RoleMaster(models.Model):
    role_name = models.CharField(max_length=50, unique=True)
    role_description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'role_master'
    

class LoginDetails(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=100)
    last_login = models.DateTimeField(auto_now=True)
    role = models.ForeignKey(RoleMaster, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'login_details'