from django.db import models
from django.test import TestCase
from grades.models import Curriculum, Grade, Path, Stage
from users.models import Student, User


class StudentModelTest(TestCase):
    def setUp(self) -> None:
        self.curriculum: Curriculum = Curriculum.objects.create(
            name="National Egyptian Curriculum"
        )
        self.path = Path.objects.create(
            curriculum=self.curriculum,
            name="English Language Path",
        )
        self.stage: Stage = Stage.objects.create(
            path=self.path, name="Secondary School", order_in_path=3
        )
        self.user: User = User.objects.create_user(
            email="student@example.com",
            username="studentuser",
            password="studentpass123",
            role=User.Role.STUDENT,
        )
        self.grade: Grade = Grade.objects.create(
            stage=self.stage, name="First year of secondary school", order_in_stage=1
        )

    def test_create_student(self) -> None:
        student: Student = Student.objects.create(user=self.user, grade=self.grade)
        self.assertEqual(student.user, self.user)
        self.assertEqual(student.grade, self.grade)

    def test_student_str_method(self) -> None:
        student: Student = Student.objects.create(user=self.user, grade=self.grade)
        self.assertEqual(str(student), self.user.username)

    def test_get_full_name(self) -> None:
        self.user.first_name = "John"
        self.user.last_name = "Doe"
        self.user.save()
        student: Student = Student.objects.create(user=self.user, grade=self.grade)
        self.assertEqual(student.get_full_name(), "John Doe")

    def test_get_short_name(self) -> None:
        self.user.first_name = "John"
        self.user.save()
        student: Student = Student.objects.create(user=self.user, grade=self.grade)
        self.assertEqual(student.get_short_name(), "John")

    def test_student_user_relationship(self) -> None:
        student: Student = Student.objects.create(user=self.user, grade=self.grade)
        self.assertTrue(hasattr(self.user, "student"))
        self.assertEqual(self.user.student, student)

    def test_student_grade_relationship(self) -> None:
        student: Student = Student.objects.create(user=self.user, grade=self.grade)
        self.assertIn(student, self.grade.students.all())

    def test_delete_user_cascades_to_student(self) -> None:
        student: Student = Student.objects.create(user=self.user, grade=self.grade)
        self.user.delete()
        with self.assertRaises(Student.DoesNotExist):
            Student.objects.get(pk=student.pk)

    def test_cannot_delete_grade_with_students(self) -> None:
        Student.objects.create(user=self.user, grade=self.grade)
        with self.assertRaises(models.deletion.ProtectedError):
            self.grade.delete()
