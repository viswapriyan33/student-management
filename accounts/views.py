from django.shortcuts import render, redirect
from django.contrib import messages
from .models import LoginDetails


def login_view(request):
    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "forgot_password":
            username = request.POST.get("username")
            old_password = request.POST.get("old_password")
            new_password = request.POST.get("new_password")
            confirm_new_password = request.POST.get("confirm_new_password")

            try:
                user = LoginDetails.objects.get(username=username, password=old_password)
            except LoginDetails.DoesNotExist:
                messages.error(request, "Invalid username or old password")
                return render(request, "accounts/login.html")

            if not new_password or new_password != confirm_new_password:
                messages.error(request, "New password and confirm password must match")
                return render(request, "accounts/login.html")

            user.password = new_password
            user.save(update_fields=["password"])
            messages.success(request, "Password changed successfully")
            return render(request, "accounts/login.html")

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