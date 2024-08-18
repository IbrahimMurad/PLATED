from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from .models import Exam, StudentAnswer
from .forms import ExamForm
from questions.models import Answer
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import exam_kwargs, get_exam_questions, get_exam_title


@login_required(login_url='login')
def generate_exam(request):
    focus = request.POST.get('focus')
    id = request.POST.get('id')
    if focus and id:
        questions = get_exam_questions(request.user.student.grade, focus, id)
        exam = Exam.objects.create(**exam_kwargs(request.user.student, focus, id))
        exam.questions.set(questions)
        exam.save()
        context = {'success': True, 'exam_id': exam.id}
    else:
        context = {'success': False}
    return render(request, 'exams/generate_exam.html', context)


@login_required(login_url='login')
def exam(request, id):
    exam = get_object_or_404(Exam, pk=id)
    if request.method == 'POST':
        form = ExamForm(exam, request.POST)
        if form.is_valid():
            score = 0
            for question in exam.questions.all():
                answer_id = form.cleaned_data['question_%s' % question.id]
                answer = get_object_or_404(Answer, pk=answer_id)
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
            messages.success(request, "Your answers have been corrected successfully.")
            return redirect('solved-exam', id=exam.id)
        else:
            messages.error("Something went wrong while correcting your answers. Please try again later.")
            return redirect('exams')
    
    return render(request, 'exams/exam.html', {
        'exam': exam,
        'title': get_exam_title(exam),
        'form': ExamForm(exam)
        })


@login_required(login_url='login')
def solved_exam(request, id):
    exam = Exam.objects.get(id=id)
    context = {
        'exam': exam,
        'title': get_exam_title(exam),
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
    }
    return render(request, 'exams/solved_exam.html', context)


@login_required(login_url='login')
def exam_list(request):
    all_exams = Exam.objects.all().order_by('-created_at')
    paginator = Paginator(all_exams, 12)
    page_number = request.GET.get('page')
    page_exams = paginator.get_page(page_number)
    return render(request, 'exams/exam_list.html', {'exams': page_exams})


@login_required(login_url='login')
def delete_exam(request, id):
    exam = get_object_or_404(Exam, id=id)
    exam.delete()
    return redirect('exams')
