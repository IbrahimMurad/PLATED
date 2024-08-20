from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Exam, StudentAnswer
from .forms import ExamForm
from questions.models import Answer
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import (
    get_exam_title,
    get_options,
    new_exam,
    exam_list_filter,
)


@login_required(login_url='login')
def generate_exam(request):
    focus = request.POST.get('focus')
    id = request.POST.get('id')
    if focus and id:
        exam = new_exam(request.user.student, focus, id)
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
            exam.solved_at = timezone.now()
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
    print(request.build_absolute_uri().split('page=')[0])
    focus = request.GET.get('focus')
    on = request.GET.get('filter_id')
    is_solved = request.GET.get('is_solved')
    all_exams = Exam.objects.filter(student=request.user.student).order_by('-created_at')
    if focus or on or is_solved:
        all_exams = exam_list_filter(all_exams, focus, on, is_solved)
    paginator = Paginator(all_exams, 12)
    page_number = request.GET.get('page')
    page_exams = paginator.get_page(page_number)
    url = request.build_absolute_uri().split('page=')[0]
    if url.endswith('/'):
        url = url + '?'
    elif url.endswith('?') or url.endswith('&'):
        url = url
    else:
        url = url + '&'
    return render(request, 'exams/exam_list.html', {
        'exams': page_exams,
        'grade_id': request.user.student.grade.id,
        'url': url,
        })


@login_required(login_url='login')
def delete_exam(request, id):
    exam = get_object_or_404(Exam, id=id)
    exam.delete()
    return redirect('exams')


def get_focus_instances(request):
    from curriculum.models import Grade
    focus = request.GET.get('focus')
    grade_id = request.GET.get('grade')
    print(focus, grade_id)
    grade = get_object_or_404(Grade, pk=grade_id)
    options = get_options(grade, focus)
    return JsonResponse(
        {
            'options': [{'id': option.id, 'name': str(option)} for option in options]
        }
    )
