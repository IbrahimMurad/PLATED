from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.test import TestCase
from grades.models import Semester
from resources.models import Chapter, Lesson, ResourceBase, Subject, TextBook, Unit


class LessonModelTest(TestCase):
    def setUp(self):
        self.physics = Subject.objects.create(name="Physics")
        self.physics_for_1st_sec = TextBook.objects.create(
            subject=self.physics,
            title="Physics for 1st secondary school",
        )
        self.linear_motion = Unit.objects.create(
            text_book=self.physics_for_1st_sec, title="Linear Motion"
        )
        self.motion_1D = Chapter.objects.create(
            unit=self.linear_motion,
            title="Motion in one dimension",
            syllabus_order=1,
        )
        self.motion_with_acceleration = Chapter.objects.create(
            unit=self.linear_motion,
            title="Motion with acceleration",
            syllabus_order=2,
        )
        self.force_and_motion = Chapter.objects.create(
            unit=self.linear_motion,
            title="Force and Motion",
            syllabus_order=3,
        )
        self.semester = Semester.objects.create()  # first semester
        self.motion = Lesson.objects.create(
            title="Motion",
            chapter=self.motion_1D,
            semester=self.semester,
            intro="Introduction to motion",
            goals="Understand motion",
            details="Details on motion",
            syllabus_order=1,
        )
        self.speed = Lesson.objects.create(
            title="Speed",
            chapter=self.motion_1D,
            semester=self.semester,
            intro="Introduction to speed",
            goals="Understand speed",
            details="Details on speed",
            syllabus_order=2,
        )
        self.acceleration = Lesson.objects.create(
            title="Acceleration",
            chapter=self.motion_1D,
            semester=self.semester,
            intro="Introduction to acceleration",
            goals="Understand acceleration",
            details="Details on acceleration",
            syllabus_order=3,
        )
        self.kinematics = Lesson.objects.create(
            title="Kinematic equatons",
            chapter=self.motion_with_acceleration,
            semester=self.semester,
            intro="Introduction to kinematic equations",
            goals="Understand kinematic equations",
            details="Details on kinematic equations",
            syllabus_order=1,
        )
        self.free_fall = Lesson.objects.create(
            title="Free fall",
            chapter=self.motion_with_acceleration,
            semester=self.semester,
            intro="Introduction to free fall",
            goals="Understand free fall",
            details="Details on free fall",
            syllabus_order=2,
        )
        self.projectiles = Lesson.objects.create(
            title="Projectiles",
            chapter=self.motion_with_acceleration,
            semester=self.semester,
            intro="Introduction to projectiles",
            goals="Understand projectiles",
            details="Details on projectiles",
            syllabus_order=3,
        )
        self.force = Lesson.objects.create(
            title="Force",
            chapter=self.force_and_motion,
            semester=self.semester,
            intro="Introduction to force",
            goals="Understand force",
            details="Details on force",
            syllabus_order=1,
        )

    def test_lesson_creation(self):
        self.assertEqual(self.motion.title, "Motion")
        self.assertEqual(self.motion.chapter, self.motion_1D)
        self.assertEqual(self.motion.semester, self.semester)
        self.assertEqual(self.motion.intro, "Introduction to motion")
        self.assertEqual(self.motion.goals, "Understand motion")
        self.assertEqual(self.motion.details, "Details on motion")
        self.assertEqual(self.motion.syllabus_order, 1)

    def test_lesson_is_subclass_of_resources(self):
        self.assertIsInstance(self.motion, Lesson)
        self.assertTrue(issubclass(Lesson, ResourceBase))

    def test_lesson_title_is_required(self):
        with self.assertRaises(ValidationError):
            Lesson.objects.create(
                chapter=self.motion_1D,
                semester=self.semester,
                intro="Introduction to motion",
                goals="Understand motion",
                details="Details on motion",
                syllabus_order=1,
            )

    def test_lesson_chapter_is_required(self):
        with self.assertRaises(ValidationError):
            Lesson.objects.create(
                title="Motion",
                semester=self.semester,
                intro="Introduction to motion",
                goals="Understand motion",
                details="Details on motion",
                syllabus_order=1,
            )

    def test_lesson_semester_is_required(self):
        with self.assertRaises(ValidationError):
            Lesson.objects.create(
                title="Motion",
                chapter=self.motion_1D,
                intro="Introduction to motion",
                goals="Understand motion",
                details="Details on motion",
                syllabus_order=1,
            )

    def test_chapter_on_delete_cascade(self):
        self.motion_1D.delete()
        self.motion_1D.save()
        self.motion_1D.refresh_from_db()
        self.assertEqual(Lesson.objects.filter(chapter=self.motion_1D).count(), 0)
        self.assertEqual(
            Lesson.objects.values_list("chapter", flat=True).distinct().count(), 2
        )
        self.assertEqual(Lesson.objects.count(), 4)
        self.assertEqual(
            list(Lesson.objects.all()),
            [
                self.kinematics,
                self.free_fall,
                self.projectiles,
                self.force,
            ],
        )

    def test_lesson_order(self):
        """tests the order of the lessons,
        should be ordered by chapter syllabus_oder first, then lesson syllabus_odrer."""
        self.assertEqual(
            list(Lesson.objects.all()),
            [
                self.motion,  # chapter 1, order 1
                self.speed,  # chapter 1, order 2
                self.acceleration,  # chapter 1, order 3
                self.kinematics,  # chapter 2, order 1
                self.free_fall,  # chapter 2, order 2
                self.projectiles,  # chapter 2, order 3
                self.force,  # chapter 3, order 1
            ],
        )

    def test_lesson_lecture_vid_path(self):
        path = self.motion.lecture_vid.field.upload_to(self.motion, "lecture.mp4")
        self.assertRegex(path, r"videos\/lessons\/lectures\/Motion.(.*).mp4")

    def test_lesson_section_vid_path(self):
        path = self.motion.section_vid.field.upload_to(self.motion, "section.mp4")
        self.assertRegex(path, r"videos\/lessons\/sections\/Motion.(.*).mp4")

    def test_add_lesson_to_requires(self):
        self.acceleration.add_lesson_to_requires(self.motion)
        self.acceleration.add_lesson_to_requires(self.speed)
        self.assertEqual(self.acceleration.requires.count(), 2)
        self.assertIn(self.speed, self.acceleration.requires.all())
        self.assertIn(self.motion, self.acceleration.requires.all())
        self.assertIn(self.acceleration, self.motion.required_by.all())

    def test_add_lesson_to_requires_validation_error(self):
        self.acceleration.add_lesson_to_requires(self.motion)
        with self.assertRaises(ValidationError):
            self.motion.add_lesson_to_requires(self.acceleration)

    def test_unique_chapter_order_constraint(self):
        with self.assertRaises(ValidationError):
            Lesson.objects.create(
                title="Force",
                chapter=self.force_and_motion,
                semester=self.semester,
                intro="Introduction to force",
                goals="Understand force",
                details="Details on force",
                syllabus_order=1,
            )

    def test_requires_lessons_are_not_required_by(self):
        self.acceleration.add_lesson_to_requires(self.motion)
        self.acceleration.add_lesson_to_requires(self.speed)
        with self.assertRaises(ValidationError):
            self.motion.add_lesson_to_requires(self.acceleration)

    def test_deleting_semester(self):
        self.semester.delete()
        all_lessons: QuerySet = Lesson.objects.all()
        self.assertIsNone(all_lessons[0].semester)
        self.acceleration.refresh_from_db()
        self.assertIsNone(self.acceleration.semester)
        self.assertEqual(all_lessons.count(), 7)

    def test_all_lessons_in_chapter(self):
        self.assertEqual(
            list(self.motion_1D.lessons.all()),
            [self.motion, self.speed, self.acceleration],
        )

    def test_lesson_str(self):
        self.assertEqual(str(self.motion), "Motion")
