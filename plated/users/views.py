from django.shortcuts import render, redirect
from django.contrib.messages import success
from django.contrib.auth.decorators import login_required
from curriculum.models import CURRENT_SEMESTER
from users.forms import (
    UserRegisterForm,
    StudentRegisterForm,
    UserUpdateForm,
    StudentUpdateForm,
)



def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        s_form = StudentRegisterForm(request.POST)

        if u_form.is_valid() and s_form.is_valid():
            user = u_form.save()
            
            student = s_form.save(commit=False)
            student.user = user
            student.save()

            success(request, f'Your account has been created! You are now able to log in!')
            return redirect('login')
    else:
        u_form = UserRegisterForm()
        s_form = StudentRegisterForm()
    return render(request, 'users/register.html', {
        'user_form': u_form,
        'student_form': s_form,
        })


@login_required(login_url='login')
def settings(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        s_form = StudentUpdateForm(request.POST, instance=request.user.student)

        if u_form.is_valid() and s_form.is_valid():
            u_form.save()
            s_form.save()
            success(request, f'Your account has been updated!')
            return redirect('settings')
    else:
        u_form = UserUpdateForm(instance=request.user)
        s_form = StudentUpdateForm(instance=request.user.student)

    return render(request, 'users/settings.html', {
        'user_form': u_form,
        'student_form': s_form,
        'semester': CURRENT_SEMESTER,
        })
