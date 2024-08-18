from subjects.models import Lesson


def get_relevant_chapter_lessons(chapter_id, grade, semester):
    return Lesson.objects.filter(
        grade=grade,
        semester=semester,
        chapter__id=chapter_id
        )


def get_relevant_unit_chapters(unit_id, grade, semester):
    lessons = Lesson.objects.filter(
        grade=grade,
        semester=semester,
        chapter__unit__id=unit_id
        )
    return list(set([lesson.chapter for lesson in lessons]))


def get_relevant_subject_units(subject_id, grade, semester):
    lessons = Lesson.objects.filter(
        grade=grade,
        semester=semester,
        chapter__unit__subject__id=subject_id
        )
    return list(set([lesson.chapter.unit for lesson in lessons]))
