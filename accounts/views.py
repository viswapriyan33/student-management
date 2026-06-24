from django.shortcuts import render, redirect
from django.contrib import messages
from .models import LoginDetails


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = LoginDetails.objects.get(username=username, password=password)
            request.session["user_id"] = user.id
            request.session["username"] = user.username
            request.session["role"] = user.role.role_name.lower()

            role_name = user.role.role_name.lower()
            if role_name == "admin":
                return redirect("teachers:admin_dashboard")
            elif role_name == "teacher":
                return redirect("teachers:teacher_dashboard")
            elif role_name == "student":
                return redirect("students:student_dashboard")

        except LoginDetails.DoesNotExist:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")