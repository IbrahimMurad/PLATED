import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Subject, Unit, Chapter, Lesson
from curriculum.models import CURRENT_SEMESTER
from django.contrib.auth.decorators import login_required
from exams.forms import GenerateExamForm
from subjects.utils import (
    get_relevant_subject_units,
    get_relevant_unit_chapters,
    get_relevant_chapter_lessons,
)


@login_required(login_url='login')
def subjects_view(request):
    if not CURRENT_SEMESTER:
        return render(request, 'subjects/chapters.html', {'message': 'There is no running semester right now.'})
    lessons = Lesson.objects.filter(grade=request.user.student.grade, semester=CURRENT_SEMESTER)
    subjects = list(set([lesson.chapter.unit.subject for lesson in lessons]))
    return render(request, 'subjects/subjects.html', {
        'subjects': subjects,
        'title': 'subjects',
        })


@login_required(login_url='login')
def units_view(request, id):
    if not CURRENT_SEMESTER:
        return render(request, 'subjects/units.html', {'message': 'There is no running semester right now.'})

    subject = get_object_or_404(Subject, pk=id)
    units = get_relevant_subject_units(id, request.user.student.grade, CURRENT_SEMESTER)

    if not units:
        return render(request, 'subjects/units.html', {
            'message': 'This subject is not available for your grade or the running semester.',
            'semester': CURRENT_SEMESTER
            })

    exam_form = GenerateExamForm(initial={'focus': 'subject', 'id': id})
    context = {
        'subject_id': subject.id,
        'title': subject.title,
        'units': units,
        'exam_form': exam_form,
    }

    return render(request, 'subjects/units.html', context)


@login_required(login_url='login')
def chapters_view(request, id):
    if not CURRENT_SEMESTER:
        return render(request, 'subjects/chapters.html', {'message': 'There is no running semester right now.'})

    unit = get_object_or_404(Unit, pk=id)
    chapters = get_relevant_unit_chapters(id, request.user.student.grade, CURRENT_SEMESTER)

    if not chapters:
        return render(request, 'subjects/chapters.html', {
            'message': 'This unit is not available for your grade or the running semester.',
            'semester': CURRENT_SEMESTER
            })

    exam_form = GenerateExamForm(initial={'focus': 'unit', 'id': id})

    context = {
        'unit': unit,
        'chapters': chapters,
        'title': unit.title,
        'exam_form': exam_form,
    }
    return render(request, 'subjects/chapters.html', context)


@login_required(login_url='login')
def lessons_view(request, id):
    if not CURRENT_SEMESTER:
        return render(request, 'subjects/chapters.html', {'message': 'There is no running semester right now.'})

    chapter = get_object_or_404(Chapter, pk=id)
    lessons = get_relevant_chapter_lessons(id, request.user.student.grade, CURRENT_SEMESTER)

    if not lessons:
        return render(request, 'subjects/lessons.html', {
            'message': 'This chapter is not available for your grade or the running semester.',
            'semester': CURRENT_SEMESTER
            })

    exam_form = GenerateExamForm(initial={'focus': 'chapter', 'id': id})

    context = {
        'chapter': chapter,
        'lessons': lessons,
        'title': chapter.title,
        'exam_form': exam_form
    }

    return render(request, 'subjects/lessons.html', context)


@login_required(login_url='login')
def lesson_details_view(request, id):
    if not CURRENT_SEMESTER:
        return render(request, 'subjects/lesson_details.html', {'message': 'There is no running semester right now.'})

    lesson = get_object_or_404(Lesson, pk=id)

    if lesson.grade != request.user.student.grade or lesson.semester != CURRENT_SEMESTER:
        return render(request, 'subjects/lesson_details.html', {
            'message': 'This lesson is not available for your grade or the running smester.',
            })

    exam_form = GenerateExamForm(initial={'focus': 'lesson', 'id': lesson.id})
    context = {
        'lesson': lesson,
        'title': lesson.title,
        'exam_form': exam_form,
    }
    return render(request, 'subjects/lesson_details.html', context)

@login_required(login_url='login')
def tag_lesson_view(request, id):
    if request.method == 'POST':
        is_bookmarked = json.loads(request.body.decode('utf-8')).get('is_bookmarked')
        try:
            lesson = Lesson.objects.get(id=id)
            student = request.user.student
            if is_bookmarked:
                lesson.tagged_students.add(student)
            else:
                lesson.tagged_students.remove(student)
            print(student.tagged_lessons.all())
            return JsonResponse({'success': True})
        except Lesson.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Lesson not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})
