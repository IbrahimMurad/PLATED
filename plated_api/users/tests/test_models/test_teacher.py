from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase
from resources.models import Subject
from users.models import Teacher, User


class TeacherModelTest(TestCase):
    def setUp(self) -> None:
        self.user: User = User.objects.create_user(
            email="teacher@example.com",
            username="teacheruser",
            password="teacherpass123",
            role=User.Role.TEACHER,
        )
        self.subject: Subject = Subject.objects.create(name="Mathematics")

    def test_create_teacher(self) -> None:
        teacher: Teacher = Teacher.objects.create(
            user=self.user, subject=self.subject, max_students=30
        )
        self.assertEqual(teacher.user, self.user)
        self.assertEqual(teacher.subject, self.subject)
        self.assertEqual(teacher.max_students, 30)

    def test_teacher_str_method(self) -> None:
        teacher: Teacher = Teacher.objects.create(user=self.user, subject=self.subject)
        self.assertEqual(str(teacher), self.user.username)

    def test_get_full_name(self) -> None:
        self.user.first_name = "Jane"
        self.user.last_name = "Smith"
        self.user.save()
        teacher: Teacher = Teacher.objects.create(user=self.user, subject=self.subject)
        self.assertEqual(teacher.get_full_name(), "Jane Smith")

    def test_get_short_name(self) -> None:
        self.user.first_name = "Jane"
        self.user.save()
        teacher: Teacher = Teacher.objects.create(user=self.user, subject=self.subject)
        self.assertEqual(teacher.get_short_name(), "Jane")

    def test_teacher_user_relationship(self) -> None:
        teacher: Teacher = Teacher.objects.create(user=self.user, subject=self.subject)
        self.assertTrue(hasattr(self.user, "teacher"))
        self.assertEqual(self.user.teacher, teacher)

    def test_teacher_subject_relationship(self) -> None:
        teacher: Teacher = Teacher.objects.create(user=self.user, subject=self.subject)
        self.assertIn(teacher, self.subject.teachers.all())

    def test_delete_user_cascades_to_teacher(self) -> None:
        teacher: Teacher = Teacher.objects.create(user=self.user, subject=self.subject)
        self.user.delete()
        with self.assertRaises(Teacher.DoesNotExist):
            Teacher.objects.get(pk=teacher.pk)

    def test_cannot_delete_subject_with_teachers(self) -> None:
        Teacher.objects.create(user=self.user, subject=self.subject)
        with self.assertRaises(models.deletion.ProtectedError):
            self.subject.delete()

    def test_max_students_default(self) -> None:
        teacher: Teacher = Teacher.objects.create(user=self.user, subject=self.subject)
        self.assertEqual(teacher.max_students, 10)

    def test_max_students_custom(self) -> None:
        teacher: Teacher = Teacher.objects.create(
            user=self.user, subject=self.subject, max_students=50
        )
        self.assertEqual(teacher.max_students, 50)

    def test_max_students_non_negative(self) -> None:
        with self.assertRaises(ValidationError):
            Teacher.objects.create(
                user=self.user, subject=self.subject, max_students=-1
            )
