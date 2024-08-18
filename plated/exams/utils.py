from datetime import timedelta
from django.shortcuts import get_object_or_404
from subjects.models import Subject, Unit, Chapter, Lesson
import random


models = {
    'subject': Subject,
    'unit': Unit,
    'chapter': Chapter,
    'lesson': Lesson,
}


def exam_kwargs(student ,focus, id):
    durations = {
        'subject': 120,
        'unit': 90,
        'chapter': 60,
        'lesson': 30,
    }
    kwargs = {
        'student': student,
        'duration': timedelta(minutes=durations[focus]),
    }
    kwargs[focus] = get_object_or_404(models[focus], pk=id)
    return kwargs


def get_all_relevant_questions(grade, focus, id):
    focus_condition = {
        'subject': 'chapter__unit__subject',
        'unit': 'chapter__unit',
        'chapter': 'chapter',
    }

    if focus == 'lesson':
        return Lesson.objects.get(pk=id).questions.all()

    focus_instance = get_object_or_404(models[focus], pk=id)

    lessons = Lesson.objects.filter(
        grade=grade,
        **{focus_condition[focus]: focus_instance},
    )

    questions = []
    [questions.extend(lesson.questions.all()) for lesson in lessons]

    return questions


def get_exam_questions(grade, focus, id):
    questions_per_exam = {
        'subject': 50,
        'unit': 40,
        'chapter': 25,
        'lesson': 10,
    }
    all_questions = get_all_relevant_questions(grade, focus, id)
    if len(all_questions) < questions_per_exam[focus]:
        return all_questions
    all_questions = list(all_questions)
    random.shuffle(all_questions)
    return all_questions[:questions_per_exam[focus]]


def get_exam_title(exam):
    exam_by = f"{exam.student.first_name} {exam.student.last_name}"
    if exam.subject:
        exam_for = exam.subject.name
    else:
        focus = exam.unit or exam.chapter or exam.lesson
        exam_for = focus.title
    return f"Exam for {exam_for} by {exam_by}"
