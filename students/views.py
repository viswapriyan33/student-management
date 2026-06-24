from django.shortcuts import render, redirect
from .models import Student

def student_dashboard(request):
    if request.session.get('role') != 'student':
        return redirect('accounts:login')

    username = request.session.get('username')
    student = Student.objects.filter(login_id=username).first()
    if not student:
        return redirect('accounts:login')

    teacher_name = student.assigned_teacher.name if student.assigned_teacher else 'Not assigned'
    percentage = student.percentage()
    pass_fail = 'Pass' if student.passed() else 'Fail'

    return render(request, 'student_dashboard.html', {
        'student': student,
        'teacher_name': teacher_name,
        'percentage': percentage,
        'pass_fail': pass_fail,
    })
