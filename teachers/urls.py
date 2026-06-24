from django.urls import path
from . import views

app_name = 'teachers'
urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add_teacher/', views.add_teacher, name='add_teacher'),
    path('edit_teacher/<int:pk>/', views.edit_teacher, name='edit_teacher'),
    path('delete_teacher/<int:pk>/', views.delete_teacher, name='delete_teacher'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('update_marks/<int:pk>/', views.update_marks, name='update_marks'),
]
