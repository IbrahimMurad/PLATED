from PIL import Image


def resize_image(imgPath):
    """ resize image """
    try:
        image = Image.open(imgPath)
        if image.height > 300 or image.width > 300:
            image.thumbnail((400, 400))
            image.save(imgPath)
    except FileNotFoundError:
        pass


def get_relevant_chapter_lessons(chapter_id, grade, semester):
    """ get relevant lessons of a chapter """
    from subjects.models import Lesson
    return Lesson.objects.filter(
        grade=grade,
        semester=semester,
        chapter__id=chapter_id
        )


def get_relevant_unit_chapters(unit_id, grade, semester):
    """ get relevant chapters of a unit """
    from subjects.models import Lesson
    lessons = Lesson.objects.filter(
        grade=grade,
        semester=semester,
        chapter__unit__id=unit_id
        )
    return list(set([lesson.chapter for lesson in lessons]))


def get_relevant_subject_units(subject_id, grade, semester):
    """ get relevant units of a subject """
    from subjects.models import Lesson
    lessons = Lesson.objects.filter(
        grade=grade,
        semester=semester,
        chapter__unit__subject__id=subject_id
        )
    return list(set([lesson.chapter.unit for lesson in lessons]))
