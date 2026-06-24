from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    login_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    assigned_teacher = models.ForeignKey('teachers.Teacher', null=True, blank=True, on_delete=models.SET_NULL)
    marks = models.IntegerField(default=0)

    def percentage(self):
        return round(self.marks, 2)

    def passed(self):
        return self.marks >= 40
