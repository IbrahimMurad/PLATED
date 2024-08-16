from django.shortcuts import render, redirect
from django.contrib.messages import success, error
from django.contrib.auth.decorators import login_required
from curriculum.models import CURRENT_SEMESTER
from users.forms import (
    UserRegisterForm,
    StudentRegisterForm,
    UserUpdateForm,
    StudentUpdateForm,
    ChangePasswordForm,
    DeleteAccountForm,
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
        user_form = UserUpdateForm(request.POST, instance=request.user)
        student_form = StudentUpdateForm(request.POST, instance=request.user.student)

        if user_form.is_valid() and student_form.is_valid():
            user_form.save()
            student_form.save()
            success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        student_form = StudentUpdateForm(instance=request.user.student)

    return render(request, 'users/settings.html', {
        'user_form': user_form,
        'student_form': student_form,
        'password_form': ChangePasswordForm(),
        'delete_form': DeleteAccountForm(),
        'semester': CURRENT_SEMESTER,
        })


@login_required(login_url='login')
def change_passowrd(request):
    if request.method == 'POST':
        password_form = ChangePasswordForm(request.POST, instance=request.user)
        if password_form.is_valid():
            request.user.set_password(password_form.cleaned_data.get('new_password'))
            request.user.save()
            success(request, f'Your password has been changed!')
            return redirect('profile')
    else:
        password_form = ChangePasswordForm()

    return render(request, 'users/settings.html', {
        'user_form': UserUpdateForm(instance=request.user),
        'student_form': StudentUpdateForm(instance=request.user.student),
        'password_form': password_form,
        'delete_form': DeleteAccountForm(),
        'semester': CURRENT_SEMESTER,
        })


@login_required(login_url='login')
def delete_account(request):
    if request.method == 'POST':
        delete_form = DeleteAccountForm(request.POST, instance=request.user)
        if delete_form.is_valid():
            request.user.delete()
            success(request, f'Your account has been deleted!')
            return redirect('login')
    else:
        delete_form = DeleteAccountForm()

    return render(request, 'users/settings.html', {
        'user_form': UserUpdateForm(instance=request.user),
        'student_form': StudentUpdateForm(instance=request.user.student),
        'password_form': ChangePasswordForm(),
        'delete_form': delete_form,
        'semester': CURRENT_SEMESTER,
        })
