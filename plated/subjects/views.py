import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from curriculum.context_processors import CURRENT_SEMESTER
from exams.forms import GenerateExamForm
from subjects.models import Chapter, Lesson, Subject, Unit
from subjects.utils import (
    get_relevant_chapter_lessons,
    get_relevant_subject_units,
    get_relevant_unit_chapters,
)


@cache_page(60 * 60)
@login_required(login_url="login")
def subjects_view(request):
    """lists all the related subjects"""

    # if there is no running semester, show a message
    if not CURRENT_SEMESTER:
        messages.error(request, "There is no running semester right now.")
        return render(request, "subjects/subjects.html")

    return render(
        request,
        "subjects/subjects.html",
        {
            "subjects": Subject.objects.filter(grade=request.user.student.grade),
            "title": "subjects",
        },
    )


@login_required(login_url="login")
def units_view(request, id):
    """lists all the related units of the subject with id=id"""

    # if there is no running semester, show a message
    if not CURRENT_SEMESTER:
        messages.error(request, "There is no running semester right now.")
        return redirect("subjects-list")

    # get the subject with id=id and query only the related units
    subject = get_object_or_404(Subject, pk=id)
    if subject.grade != request.user.student.grade:
        messages.error(request, "This subject is not available for your grade.")
        return redirect("subjects-list")

    units = Unit.relevant.filter(subject=subject)

    # if there are no related units in this subject, show a message
    if not units.exists():
        messages.error(request, "This subject has no units for the running semester.")
        return render(
            request,
            "subjects/units.html",
            {"subject_id": subject.id, "title": subject.title},
        )

    # create a form to generate exams (for the generate exam button)
    exam_form = GenerateExamForm(initial={"focus": "subject", "id": id})
    context = {
        "subject_id": subject.id,
        "title": subject.title,
        "units": units,
        "exam_form": exam_form,
    }

    return render(request, "subjects/units.html", context)


@cache_page(60 * 60)
@login_required(login_url="login")
def chapters_view(request, id):
    """lists all the related chapters of the unit with id=id"""
    if not CURRENT_SEMESTER:
        return render(
            request,
            "subjects/chapters.html",
            {"message": "There is no running semester right now."},
        )

    unit = get_object_or_404(Unit, pk=id)
    chapters = get_relevant_unit_chapters(
        id, request.user.student.grade, CURRENT_SEMESTER
    )

    # if there are no related chapters in this unit, show a message
    if not chapters:
        return render(
            request,
            "subjects/chapters.html",
            {
                "message": "This unit is not available for your grade or the running semester.",
            },
        )

    # create a form to generate exams (for the generate exam button)
    exam_form = GenerateExamForm(initial={"focus": "unit", "id": id})

    context = {
        "unit": unit,
        "chapters": chapters,
        "title": unit.title,
        "exam_form": exam_form,
    }
    return render(request, "subjects/chapters.html", context)


@cache_page(60 * 60)
@login_required(login_url="login")
def lessons_view(request, id):
    """lists all the related lessons of the chapter with id=id"""
    if not CURRENT_SEMESTER:
        return render(
            request,
            "subjects/chapters.html",
            {"message": "There is no running semester right now."},
        )

    chapter = get_object_or_404(Chapter, pk=id)
    lessons = get_relevant_chapter_lessons(
        id, request.user.student.grade, CURRENT_SEMESTER
    )

    # if there are no related lessons in this chapter, show a message
    if not lessons:
        return render(
            request,
            "subjects/lessons.html",
            {
                "message": "This chapter is not available for your grade or the running semester.",
            },
        )

    # create a form to generate exams (for the generate exam button)
    exam_form = GenerateExamForm(initial={"focus": "chapter", "id": id})

    context = {
        "chapter": chapter,
        "lessons": lessons,
        "title": chapter.title,
        "exam_form": exam_form,
    }

    return render(request, "subjects/lessons.html", context)


@login_required(login_url="login")
def lesson_details_view(request, id):
    """show the details of a lesson"""

    # if there is no running semester, show a message
    if not CURRENT_SEMESTER:
        return render(
            request,
            "subjects/lesson_details.html",
            {"message": "There is no running semester right now."},
        )

    lesson = get_object_or_404(Lesson, pk=id)

    # if the lesson is not related, show a message
    if (
        lesson.grade != request.user.student.grade
        or lesson.semester != CURRENT_SEMESTER
    ):
        return render(
            request,
            "subjects/lesson_details.html",
            {
                "message": "This lesson is not available for your grade or the running smester.",
            },
        )

    # create a form to generate exams (for the generate exam button)
    exam_form = GenerateExamForm(initial={"focus": "lesson", "id": lesson.id})
    context = {
        "lesson": lesson,
        "title": lesson.title,
        "exam_form": exam_form,
    }
    return render(request, "subjects/lesson_details.html", context)


@cache_page(60 * 60)
@login_required(login_url="login")
def tag_lesson_view(request, id):
    """tag/untag a lesson when the bookmark button is clicked"""

    if request.method == "POST":
        is_bookmarked = json.loads(request.body.decode("utf-8")).get("is_bookmarked")
        try:
            lesson = Lesson.objects.get(id=id)
            student = request.user.student
            if is_bookmarked:
                lesson.tagged_students.add(student)
            else:
                lesson.tagged_students.remove(student)
            return JsonResponse({"success": True})
        except Lesson.DoesNotExist:
            return JsonResponse({"success": False, "error": "Lesson not found"})

    return JsonResponse({"success": False, "error": "Invalid request method"})
