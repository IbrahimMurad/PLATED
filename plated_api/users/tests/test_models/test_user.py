from django.db import IntegrityError
from django.test import TestCase
from users.models import User


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email="test@example.com", username="testuser", password="testpass123"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertEqual(user.role, User.Role.ADMIN)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email="admin@example.com", username="admin", password="adminpass123"
        )
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertEqual(admin_user.username, "admin")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertEqual(admin_user.role, User.Role.ADMIN)

    def test_email_is_unique(self):
        User.objects.create_user(
            email="unique@example.com", username="user1", password="pass123"
        )
        with self.assertRaises(IntegrityError):
            User.objects.create_user(
                email="unique@example.com", username="user2", password="pass123"
            )

    def test_username_is_not_unique(self):
        User.objects.create_user(
            email="user1@example.com", username="sameuser", password="pass123"
        )
        User.objects.create_user(
            email="user2@example.com", username="sameuser", password="pass123"
        )
        self.assertEqual(User.objects.filter(username="sameuser").count(), 2)

    def test_user_roles(self):
        admin = User.objects.create_user(
            email="admin@example.com",
            username="admin",
            password="pass123",
            role=User.Role.ADMIN,
        )
        student = User.objects.create_user(
            email="student@example.com",
            username="student",
            password="pass123",
            role=User.Role.STUDENT,
        )
        teacher = User.objects.create_user(
            email="teacher@example.com",
            username="teacher",
            password="pass123",
            role=User.Role.TEACHER,
        )

        self.assertTrue(admin.is_admin())
        self.assertFalse(admin.is_student())
        self.assertFalse(admin.is_teacher())

        self.assertFalse(student.is_admin())
        self.assertTrue(student.is_student())
        self.assertFalse(student.is_teacher())

        self.assertFalse(teacher.is_admin())
        self.assertFalse(teacher.is_student())
        self.assertTrue(teacher.is_teacher())

    def test_str_method(self):
        user = User.objects.create_user(
            email="test@example.com", username="testuser", password="testpass123"
        )
        self.assertEqual(str(user), "testuser")
