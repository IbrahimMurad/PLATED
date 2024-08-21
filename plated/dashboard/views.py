from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from subjects.models import Lesson
from .utils import (
    avg_score_progress,
    score_progress,
    plot,
)

@login_required(login_url='login')
def main_dashboard_view(request):
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
    user = request.user
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
    print(context)
    return render(request, 'dashboard/subjects_dashboard.html', context)


@login_required(login_url='login')
def unit_dashboard_view(request, id):
    user = request.user
    units_scores = score_progress(user, 'unit', {'subject__id': id})
    context = {
        'units': [
            {
                'id': unit['id'],
                'title': unit['title'],
                'plot_url': plot(f"{unit['title']}_score_progress", unit['scores'], user.id),
            }
            for unit in units_scores
        ],
    }
    return render(request, 'dashboard/units_dashboard.html', context)


@login_required(login_url='login')
def chapter_dashboard_view(request, id):
    user = request.user
    chapters_scores = score_progress(user, 'chapter', {'unit__id': id})
    context = {
        'chapters': [
            {
                'id': chapter['id'],
                'title': chapter['title'],
                'plot_url': plot(f"{chapter['title']}_score_progress", chapter['scores'], user.id),
            }
            for chapter in chapters_scores
        ]
    }
    return render(request, 'dashboard/chapters_dashboard.html', context)


@login_required(login_url='login')
def lesson_dashboard_view(request, id):
    user = request.user
    lessons_scores = score_progress(user, 'lesson', {'chapter__id': id})
    context = {
        'lessons': [
            {
                'id': lesson['id'],
                'title': lesson['title'],
                'plot_url': plot(f"{lesson['title']}_score_progress", lesson['scores'], user.id),
            }
            for lesson in lessons_scores
        ]
    }
    return render(request, 'dashboard/lessons_dashboard.html', context)
