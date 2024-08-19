from datetime import timedelta
from django.shortcuts import get_object_or_404
from subjects.models import Subject, Unit, Chapter, Lesson
from .models import Exam
import random


models = {
    'subject': Subject,
    'unit': Unit,
    'chapter': Chapter,
    'lesson': Lesson,
}


focus_condition = {
    'subject': 'chapter__unit__subject',
    'unit': 'chapter__unit',
    'chapter': 'chapter',
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
        exam_for = exam.subject.title
    else:
        focus = exam.unit or exam.chapter or exam.lesson
        exam_for = focus.title
    return f"Exam for {exam_for} by {exam_by}"


def get_options(grade, focus):
    from curriculum.models import CURRENT_SEMESTER
    lessons = Lesson.objects.filter(grade=grade, semester=CURRENT_SEMESTER)
    focus_instances = {
        'subject': list(set([lesson.chapter.unit.subject for lesson in lessons])),
        'unit': list(set([lesson.chapter.unit for lesson in lessons])),
        'chapter': list(set([lesson.chapter for lesson in lessons])),
        'lesson': lessons,
    }
    return focus_instances[focus]


def new_exam(student, focus, id):
    questions = get_exam_questions(student.grade, focus, id)
    exam = Exam.objects.create(**exam_kwargs(student, focus, id))
    exam.questions.set(questions)
    exam.save()
    return exam


def exam_list_filter(focus, on, is_solved):
    exams = Exam.objects.all()
    focus_condition = {
        'subject': {'unit': None, 'chapter': None, 'lesson': None},
        'unit': {'subject': None, 'chapter': None, 'lesson': None},
        'chapter': {'unit': None, 'subject': None, 'lesson': None},
        'lesson': {'unit': None, 'chapter': None, 'subject': None},
    }
    if focus:
        exams = exams.filter(**focus_condition[focus])
        if on:
            exams = exams.filter(**{focus: models[focus].objects.get(pk=on)})
    if is_solved == 'true':
        exams = exams.filter(solved_at__isnull=False)
    elif is_solved == 'false':
        exams = exams.filter(solved_at__isnull=True)
    return exams.order_by('-created_at')
