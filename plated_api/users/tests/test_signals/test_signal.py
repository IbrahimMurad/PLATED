from django.contrib.auth.models import Group
from django.test import TestCase
from grades.models import Curriculum, Grade, Path, Stage
from resources.models import Subject
from users.models import Student, Teacher, User


class SignalsTest(TestCase):
    def setUp(self):
        # create the groups
        Group.objects.create(name="Admin")
        Group.objects.create(name="Student")
        Group.objects.create(name="Teacher")

        # create grade
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
        self.grade: Grade = Grade.objects.create(
            stage=self.stage, name="First year of secondary school", order_in_stage=1
        )

        # create subject
        self.subject: Subject = Subject.objects.create(name="Mathematics")

    def test_add_user_to_admin_group(self):
        admin_user = User.objects.create_user(
            email="admin@example.com",
            username="admin",
            password="adminpass123",
            role=User.Role.ADMIN,
        )
        self.assertTrue(admin_user.groups.filter(name="Admin").exists())

    def test_do_not_add_non_admin_to_admin_group(self):
        student_user: User = User.objects.create_user(
            email="student@example.com",
            username="student",
            password="studentpass123",
            role=User.Role.STUDENT,
        )
        self.assertFalse(student_user.groups.filter(name="Admin").exists())

    def test_add_user_to_student_group(self):
        user = User.objects.create_user(
            email="student@example.com",
            username="student",
            password="studentpass123",
            role=User.Role.STUDENT,
        )
        Student.objects.create(user=user, grade=self.grade)
        self.assertTrue(user.groups.filter(name="Student").exists())

    def test_add_user_to_teacher_group(self):
        user: User = User.objects.create_user(
            email="teacher@example.com",
            username="teacher",
            password="teacherpass123",
            role=User.Role.TEACHER,
        )
        Teacher.objects.create(user=user, subject=self.subject)
        self.assertTrue(user.groups.filter(name="Teacher").exists())
