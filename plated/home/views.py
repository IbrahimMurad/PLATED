from django.shortcuts import render
from exams.models import Exam
from django.db import models


def home(request):
    student = request.user.student
    solved_exams = Exam.objects.filter(student=student, score__isnull=False).order_by('-solved_at')
    recent_solved_exams = solved_exams[:3]
    unsolved_exams = Exam.objects.filter(student=student, score__isnull=True).order_by('-created_at')[:3]
    total_score = solved_exams.aggregate(total_score=models.Sum('score'))['total_score']
    total_max_score = sum([exam.max_score for exam in solved_exams])
    average_score = total_score / total_max_score * 100 if total_max_score else 0
    score_color = 'red' if average_score < 75 else 'green'
    print(total_score, total_max_score)
    return render(request, 'home/home.html', {
        'recent_solved_exams': recent_solved_exams,
        'unsolved_exams': unsolved_exams,
        'average_score': average_score,
        'score_color': 'color: ' + score_color,
        'tagged_lessons': student.tagged_lessons.all()
        })
