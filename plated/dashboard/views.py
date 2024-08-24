from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from curriculum.context_processors import CURRENT_SEMESTER
from subjects.models import Subject, Unit, Chapter, Lesson
from .utils import (
    avg_score_progress,
    score_progress,
    plot,
)

@login_required(login_url='login')
def main_dashboard_view(request):
    """ average graphs for overall, subjects, units, chapters, and lessons """
    user = request.user

    overall_progress = avg_score_progress(user, {})
    subjects_progress = avg_score_progress(user, {'subject__isnull': False})
    units_progress = avg_score_progress(user, {'unit__isnull': False})
    chapters_progress = avg_score_progress(user, {'chapter__isnull': False})
    lessons_progress = avg_score_progress(user, {'lesson__isnull': False})

    context = {
        'overall_plot_url': plot('overall_avg_score_progress', overall_progress, user.id),
        'subjects_plot_url': plot('subjects_avg_score_progress', subjects_progress, user.id),
        'units_plot_url': plot('units_avg_score_progress', units_progress, user.id),
        'chapters_plot_url': plot('chapters_avg_score_progress', chapters_progress, user.id),
        'lessons_plot_url': plot('lessons_avg_score_progress', lessons_progress, user.id),
    }
    return render(request, 'dashboard/main_dashboard.html', context)


@login_required(login_url='login')
def subject_dashboard_view(request):
    """ dashboard for subjects score progress """
    user = request.user

    # get all scores of all subjects
    subjects_scores = score_progress(user, 'subject', {})
    context = {
        'subjects': [
            {
                'id': subject['id'],
                'title': subject['title'],
                'plot_url': plot(f"{subject['title']}_score_progress", subject['scores'], user.id),
                }
            for subject in subjects_scores
        ]
    }
    if not context['subjects']:
        context = {
            'subjects': [
                {
                    'id': subject.id,
                    'title': subject.title,
                    'plot_url': None,
                }
                for subject in list(set([lesson.chapter.unit.subject for lesson in Lesson.objects.filter(grade=user.student.grade)]))
            ]
        }
    return render(request, 'dashboard/subjects_dashboard.html', context)


@login_required(login_url='login')
def unit_dashboard_view(request, id):
    """ dashboard for units score progress of this subejct """
    user = request.user

    if not Subject.objects.filter(id=id).exists():
        messages.error(request, "This subject does not exist.")
        return redirect('main-dashboard')

    lessons = Lesson.objects.filter(grade=user.student.grade, semester=CURRENT_SEMESTER, chapter__unit__subject__id=id)
    subject = lessons.values_list('chapter__unit__subject', flat=True).distinct()
    if not subject:
        messages.error(request, "This subject is not in your curriculum or it is not available to this semester.")
        return redirect('main-dashboard')

    units_scores = score_progress(user, 'unit', {'chapter__unit__subject__id': id})
    context = {
        'subject': Subject.objects.get(id=id),
        'units': [
            {
                'id': unit['id'],
                'title': unit['title'],
                'plot_url': plot(f"{unit['title']}_score_progress", unit['scores'], user.id) if unit['scores'] else None,
            }
            for unit in units_scores
        ],
    }
    
    return render(request, 'dashboard/units_dashboard.html', context)


@login_required(login_url='login')
def chapter_dashboard_view(request, id):
    """ dashboard for chapters score progress of this unit """
    user = request.user

    if not Unit.objects.filter(id=id).exists():
        messages.error(request, "This unit does not exist.")
        return redirect('main-dashboard')

    lessons = Lesson.objects.filter(grade=user.student.grade, semester=CURRENT_SEMESTER, chapter__unit__id=id)
    unit = lessons.values_list('chapter__unit', flat=True).distinct()
    if not unit:
        messages.error(request, "This unit is not in your curriculum or it is not available to this semester.")
        return redirect('main-dashboard')


    chapters_scores = score_progress(user, 'chapter', {'chapter__unit__id': id})
    context = {
        'unit': Unit.objects.get(id=id),
        'chapters': [
            {
                'id': chapter['id'],
                'title': chapter['title'],
                'plot_url': plot(f"{chapter['title']}_score_progress", chapter['scores'], user.id) if chapter['scores'] else None,
            }
            for chapter in chapters_scores
        ]
    }
    return render(request, 'dashboard/chapters_dashboard.html', context)


@login_required(login_url='login')
def lesson_dashboard_view(request, id):
    user = request.user

    if not Chapter.objects.filter(id=id).exists():
        messages.error(request, "This chapter does not exist.")
        return redirect('main-dashboard')

    lessons = Lesson.objects.filter(grade=user.student.grade, semester=CURRENT_SEMESTER, chapter__id=id)
    chapter = lessons.values_list('chapter', flat=True).distinct()
    if not chapter:
        messages.error(request, "This chapter is not in your curriculum or it is not available to this semester.")
        return redirect('main-dashboard')


    lessons_scores = score_progress(user, 'lesson', {'chapter__id': id})
    context = {
        'chapter': Chapter.objects.get(id=id),
        'lessons': [
            {
                'id': lesson['id'],
                'title': lesson['title'],
                'plot_url': plot(f"{lesson['title']}_score_progress", lesson['scores'], user.id) if lesson['scores'] else None,
            }
            for lesson in lessons_scores
        ]
    }
    return render(request, 'dashboard/lessons_dashboard.html', context)
