from django.urls import path
from . import views

app_name = 'students'
urlpatterns = [
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
]
