from django.core.paginator import Paginator
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from .models import Exam, StudentAnswer
from .forms import ExamForm
from questions.models import Question, Answer
from subjects.models import Lesson
from datetime import timedelta, datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DeleteView


def generate_lesson_exam(request, id):
    if request.method == 'POST':
        lesson = Lesson.objects.get(id=id)
        questions = Question.objects.filter(lesson=lesson)[:10]
        exam = Exam.objects.create(
            student=request.user.student,
            lesson=lesson,
            duration=timedelta(minutes=30)
            )
        exam.questions.set(questions)
        exam.save()

        return redirect('lesson-exam', id=exam.id)


@login_required(login_url='login')
def lesson_exam(request, id):
    exam = Exam.objects.get(id=id)
    if request.method == 'POST':
        form = ExamForm(exam, request.POST)
        if form.is_valid():
            score = 0
            for question in exam.questions.all():
                answer_id = form.cleaned_data['question_%s' % question.id]
                answer = Answer.objects.get(id=answer_id)
                student_answer = StudentAnswer.objects.create(
                    exam=exam,
                    student=request.user.student,
                    answer=answer
                    )
                student_answer.save()
                if answer.is_correct:
                    score += 1
            exam.score = score
            exam.solved_at = datetime.utcnow()
            exam.save()
            return redirect('solved-exam', id=exam.id)
        else:
            messages.error("Something went wrong while correcting your answers. Please try again later.")

    return render(request, 'exams/exam.html', {
        'exam': exam,
        'form': ExamForm(exam)
        })


@login_required(login_url='login')
def solved_exam(request, id):
    exam = Exam.objects.get(id=id)
    context = {
        'exam_id': exam.id,
        'exam_title': f"Exam on {exam.lesson.title}",
        'lesson_id': exam.lesson.id,
        'questions': [
            {
                'body': question.body,
                'answers': question.answers.all(),
                'student_answer': StudentAnswer.objects.filter(
                    student=request.user.student,
                    exam=exam,
                    answer__question=question
                    ).first()
            }
            for question in exam.questions.all()
        ],
        'score': exam.score,
        'created_at': exam.created_at,
        'solved_at': exam.solved_at
    }
    return render(request, 'exams/solved_exam.html', context)


def exam_list(request):
    all_exams = Exam.objects.all().order_by('-created_at')
    paginator = Paginator(all_exams, 12)
    page_number = request.GET.get('page')
    page_exams = paginator.get_page(page_number)
    return render(request, 'exams/exam_list.html', {'exams': page_exams})


def delecte_exam(request, id):
    exam = get_object_or_404(Exam, id=id)
    exam.delete()
    return redirect('exams')
