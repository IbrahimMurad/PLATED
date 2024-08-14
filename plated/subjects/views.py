from django.shortcuts import render
from .models import Subject, Unit, Chapter, Lesson
from curriculum.models import CURRENT_SEMESTER
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def subjects_view(request):
    subjects = Subject.objects.all()
    return render(request, 'subjects/subjects.html', {'subjects': subjects, 'semester': CURRENT_SEMESTER})

@login_required(login_url='login')
def units_view(request, id):
    subject = Subject.objects.get(pk=id)
    return render(request, 'subjects/units.html', {'subject': subject, 'semester': CURRENT_SEMESTER})

@login_required(login_url='login')
def chapters_view(request, id):
    unit = Unit.objects.get(pk=id)
    return render(request, 'subjects/chapters.html', {'unit': unit, 'semester': CURRENT_SEMESTER})

@login_required(login_url='login')
def lessons_view(request, id):
    chapter = Chapter.objects.get(pk=id)
    return render(request, 'subjects/lessons.html', {'chapter': chapter, 'semester': CURRENT_SEMESTER})

@login_required(login_url='login')
def lesson_details_view(request, id):
    lesson = Lesson.objects.get(pk=id)
    return render(request, 'subjects/lesson_details.html', {'lesson': lesson, 'semester': CURRENT_SEMESTER})
