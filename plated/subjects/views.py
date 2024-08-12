from django.shortcuts import render
from .models import Subject, Unit, Chapter, Lesson


def subjects_view(request):
    subjects = Subject.objects.all()
    return render(request, 'subjects/subjects.html', {'subjects': subjects})

def units_view(request, id):
    units = Unit.objects.filter(subject_id=id).order_by('number')
    return render(request, 'subjects/units.html', {'units': units})

def chapters_view(request, id):
    chapters = Chapter.objects.filter(unit_id=id).order_by('number')
    return render(request, 'subjects/chapters.html', {'chapters': chapters})

def lessons_view(request, id):
    lessons = Lesson.objects.filter(chapter_id=id).order_by('number')
    return render(request, 'subjects/lessons.html', {'lessons': lessons})

def lesson_details_view(request, id):
    lesson = Lesson.objects.get(id=id)
    return render(request, 'subjects/lesson_details.html', {'lesson': lesson})
