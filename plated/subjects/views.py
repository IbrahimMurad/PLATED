from django.shortcuts import render, get_object_or_404
from .models import Subject, Unit, Chapter, Lesson
from curriculum.models import CURRENT_SEMESTER
from django.contrib.auth.decorators import login_required
from exams.forms import ExamForm


@login_required(login_url='login')
def subjects_view(request):
    if not CURRENT_SEMESTER:
        return render(request, 'subjects/chapters.html', {'message': 'There is no running semester right now.'})
    lessons = Lesson.objects.filter(grade=request.user.student.grade, semester=CURRENT_SEMESTER)
    subjects = list(set([lesson.chapter.unit.subject for lesson in lessons]))
    return render(request, 'subjects/subjects.html', {
        'subjects': subjects,
        'semester': CURRENT_SEMESTER,
        'title': 'subjects',
        })


@login_required(login_url='login')
def units_view(request, id):
    if not CURRENT_SEMESTER:
        return render(request, 'subjects/units.html', {'message': 'There is no running semester right now.'})
    requested_subject = get_object_or_404(Subject, pk=id)
    lessons = Lesson.objects.filter(
        grade=request.user.student.grade,
        semester=CURRENT_SEMESTER,
        chapter__unit__subject=requested_subject
        )
    units = list(set([lesson.chapter.unit for lesson in lessons]))
    if not units:
        return render(request, 'subjects/units.html', {
            'message': 'This subject is not available for your grade or the running semester.',
            'semester': CURRENT_SEMESTER
            })
    subject = {
        'id': id,
        'name': requested_subject.name,
        'units': units,
    }
    context = {
        'subject': subject,
        'semester': CURRENT_SEMESTER,
        'title': requested_subject.name,
    }
    return render(request, 'subjects/units.html', context)


@login_required(login_url='login')
def chapters_view(request, id):
    if not CURRENT_SEMESTER:
        return render(request, 'subjects/chapters.html', {'message': 'There is no running semester right now.'})
    requested_unit = get_object_or_404(Unit, pk=id)
    lessons = Lesson.objects.filter(
        grade=request.user.student.grade,
        semester=CURRENT_SEMESTER,
        chapter__unit=requested_unit
        )
    chapters = list(set([lesson.chapter for lesson in lessons]))
    if not chapters:
        return render(request, 'subjects/chapters.html', {
            'message': 'This unit is not available for your grade or the running semester.',
            'semester': CURRENT_SEMESTER
            })
    unit = {
        'id': id,
        'title': requested_unit.title,
        'subject_id': requested_unit.subject.pk,
        'subject_name': requested_unit.subject.name,
        'chapters': chapters,
    }
    context = {
        'unit': unit,
        'semester': CURRENT_SEMESTER,
        'title': requested_unit.title,
    }
    return render(request, 'subjects/chapters.html', context)


@login_required(login_url='login')
def lessons_view(request, id):
    if not CURRENT_SEMESTER:
        return render(request, 'subjects/chapters.html', {'message': 'There is no running semester right now.'})
    requested_chapter = get_object_or_404(Chapter, pk=id)
    lessons = Lesson.objects.filter(
        grade=request.user.student.grade,
        semester=CURRENT_SEMESTER,
        chapter=requested_chapter
        )
    if not lessons:
        return render(request, 'subjects/lessons.html', {
            'message': 'This chapter is not available for your grade or the running semester.',
            'semester': CURRENT_SEMESTER
            })
    chapter = {
        'id': id,
        'title': requested_chapter.title,
        'unit_id': requested_chapter.unit.pk,
        'unit_title': requested_chapter.unit.title,
        'subject_id': requested_chapter.unit.subject.pk,
        'subject_name': requested_chapter.unit.subject.name,
        'lessons': lessons,
    }
    context = {
        'chapter': chapter,
        'semester': CURRENT_SEMESTER,
        'title': requested_chapter.title,
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
            'semester': CURRENT_SEMESTER
            })
    context = {
        'lesson': lesson,
        'title': lesson.title,
        'semester': CURRENT_SEMESTER
    }
    exams = lesson.exam_set.all()
    if exams:
        last_exam = exams.filter(student=request.user.student).order_by('-created_at').first()
        exam_form = ExamForm(last_exam)
        context.update({'exam_form': exam_form})
    return render(request, 'subjects/lesson_details.html', context)
