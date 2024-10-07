from datetime import datetime
from uuid import UUID

from django.core.exceptions import ValidationError
from django.test import TestCase
from resources.models import Subject


class TestSubject(TestCase):
    def setUp(self) -> None:
        self.math = Subject.objects.create(name="Math")
        self.physics = Subject.objects.create(name="Physics")
        self.english = Subject.objects.create(name="English")
        self.biology = Subject.objects.create(name="Biology")
        self.chemistry = Subject.objects.create(name="Chemistry")
        self.history = Subject.objects.create(name="History")
        self.geography = Subject.objects.create(name="Geography")
        self.computer_science = Subject.objects.create(name="Computer Science")
        self.economics = Subject.objects.create(name="Economics")

    def test_str(self) -> None:
        self.assertEqual(str(self.math), "Math")
        self.assertEqual(str(self.physics), "Physics")

    def test_ordering(self) -> None:
        all_subjects = Subject.objects.all()
        self.assertEqual(all_subjects[0], self.biology)
        self.assertEqual(all_subjects[1], self.chemistry)
        self.assertEqual(all_subjects[2], self.computer_science)
        self.assertEqual(all_subjects[3], self.economics)
        self.assertEqual(all_subjects[4], self.english)
        self.assertEqual(all_subjects[5], self.geography)
        self.assertEqual(all_subjects[6], self.history)
        self.assertEqual(all_subjects[7], self.math)
        self.assertEqual(all_subjects[8], self.physics)

    def test_subject_name_is_required(self) -> None:
        with self.assertRaises(ValidationError):
            Subject.objects.create(name=None)  # type: ignore

    def test_subject_name_is_unique(self) -> None:
        with self.assertRaises(ValidationError):
            Subject.objects.create(name="Math")

    def test_subject_has_id_and_it_is_uuid(self) -> None:
        self.assertIsNotNone(self.math.id)
        self.assertIsInstance(self.math.id, UUID)

    def test_subject_has_created_at_and_it_is_datetime(self) -> None:
        self.assertIsNotNone(self.math.created_at)
        self.assertIsInstance(self.math.created_at, datetime)

    def test_subject_has_updated_at_and_it_is_datetime(self) -> None:
        self.assertIsNotNone(self.math.updated_at)
        self.assertIsInstance(self.math.updated_at, datetime)
