from django.urls import path, include

urlpatterns = [
    path('', include('accounts.urls')),
    path('teachers/', include('teachers.urls')),
    path('students/', include('students.urls')),
]

