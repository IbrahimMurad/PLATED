from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from exams.models import Exam
from dashboard.utils import avg


@login_required(login_url='login')
def home(request):
    """ home view """

    student = request.user.student
    all_exams = Exam.objects.filter(student=student)

    # get recent 3 solved exams
    solved_exams = all_exams.filter(score__isnull=False).order_by('-solved_at')
    recent_solved_exams = solved_exams[:3]

    # get recent 6 unsolved exams
    unsolved_exams = all_exams.filter(score__isnull=True).order_by('-created_at')[:6]

    # get average score of all solved exams by this student and color it based on the score
    average_scores = [exam.score_percentage for exam in solved_exams]
    average_score = avg(average_scores)
    score_color = 'red' if average_score < 75 else 'green'

    return render(request, 'home/home.html', {
        'recent_solved_exams': recent_solved_exams,
        'unsolved_exams': unsolved_exams,
        'average_score': average_score,
        'score_color': 'color: ' + score_color,
        'tagged_lessons': student.tagged_lessons.all()
        })
