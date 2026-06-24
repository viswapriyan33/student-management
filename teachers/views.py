from functools import wraps

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Teacher
from students.models import Student
from accounts.models import LoginDetails, RoleMaster


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.session.get('role') != 'admin':
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def admin_dashboard(request):
    if request.method == "POST":
        form_type = request.POST.get('form_type')
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, 'Username and password are required.')
        elif LoginDetails.objects.filter(username=username).exists():
            messages.error(request, 'This username is already taken.')
        else:
            if form_type == 'teacher':
                first_name = request.POST.get('first_name', '').strip()
                last_name = request.POST.get('last_name', '').strip()
                email = request.POST.get('email', '').strip()
                subject = request.POST.get('subject', '').strip()

                if not (first_name and last_name and email and subject):
                    messages.error(request, 'All teacher fields are required.')
                else:
                    role = RoleMaster.objects.filter(role_name__iexact='teacher').first()
                    if not role:
                        role = RoleMaster.objects.create(role_name='teacher')

                    LoginDetails.objects.create(
                        username=username,
                        password=password,
                        role=role
                    )
                    Teacher.objects.create(
                        teacher_id=f"KASPON-{username}",
                        name=f"{first_name} {last_name}",
                        subject=subject,
                        email=email,
                        login_id=username,
                        password=password
                    )
                    messages.success(request, 'Teacher account created successfully.')
            elif form_type == 'student':
                first_name = request.POST.get('first_name', '').strip()
                last_name = request.POST.get('last_name', '').strip()
                email = request.POST.get('email', '').strip()
                assigned_teacher_id = request.POST.get('assigned_teacher')

                if not (first_name and last_name and email):
                    messages.error(request, 'All student fields are required.')
                else:
                    role = RoleMaster.objects.filter(role_name__iexact='student').first()
                    if not role:
                        role = RoleMaster.objects.create(role_name='student')

                    teacher = None
                    if assigned_teacher_id:
                        teacher = Teacher.objects.filter(pk=assigned_teacher_id).first()

                    LoginDetails.objects.create(
                        username=username,
                        password=password,
                        role=role
                    )
                    Student.objects.create(
                        student_id=f"KASPON-{username}",
                        name=f"{first_name} {last_name}",
                        email=email,
                        login_id=username,
                        assigned_teacher=teacher,
                        marks=0
                    )
                    messages.success(request, 'Student account created successfully.')
            else:
                messages.error(request, 'Invalid registration form submission.')

    teachers = Teacher.objects.all()
    students = Student.objects.all()
    return render(request, 'admin_dashboard.html', {'teachers': teachers, 'students': students})

# keep add_teacher for backward compatibility if needed
@admin_required
def add_teacher(request):
    if request.method == "POST":
        Teacher.objects.create(
            teacher_id=request.POST['teacher_id'],
            name=request.POST['name'],
            subject=request.POST['subject'],
            email=request.POST['email'],
            login_id=request.POST['login_id'],
            password=request.POST['password']
        )
        return redirect('teachers:admin_dashboard')
    return render(request, 'add_teacher.html')

@admin_required
def edit_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == "POST":
        teacher.name = request.POST['name']
        teacher.subject = request.POST['subject']
        teacher.email = request.POST['email']
        teacher.save()
        return redirect('teachers:admin_dashboard')
    return render(request, 'edit_teacher.html', {'teacher': teacher})

@admin_required
def delete_teacher(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    teacher.delete()
    return redirect('teachers:admin_dashboard')

def teacher_dashboard(request):
    if request.session.get('role') != 'teacher':
        return redirect('accounts:login')

    username = request.session.get('username')
    teacher = Teacher.objects.filter(login_id=username).first()
    if not teacher:
        return redirect('accounts:login')

    students = Student.objects.all()
    return render(request, 'teacher_dashboard.html', {'students': students, 'teacher': teacher})

def update_marks(request, pk):
    if request.session.get('role') != 'teacher':
        return redirect('accounts:login')

    username = request.session.get('username')
    teacher = Teacher.objects.filter(login_id=username).first()
    student = get_object_or_404(Student, pk=pk)

    if student.assigned_teacher and student.assigned_teacher != teacher:
        return redirect('teachers:teacher_dashboard')

    if request.method == "POST":
        try:
            student.marks = int(request.POST['marks'])
        except (ValueError, TypeError):
            student.marks = 0
        student.save()
        return redirect('teachers:teacher_dashboard')

    return render(request, 'update_marks.html', {'student': student, 'teacher': teacher})
