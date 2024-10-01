from datetime import date, timedelta
from uuid import UUID

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone
from grades.models import Semester


class SemesterTestCase(TestCase):
    def test_semester_with_valid_values(self):
        semester = Semester.objects.create(
            name=Semester.SemesterChoices.FIRST_TERM,
            starts_at=date(2024, 9, 1),
            ends_at=date(2024, 12, 31),
        )
        self.assertEqual(semester.name, Semester.SemesterChoices.FIRST_TERM)
        self.assertEqual(semester.starts_at, date(2024, 9, 1))
        self.assertEqual(semester.ends_at, date(2024, 12, 31))
        self.assertEqual(str(semester), Semester.SemesterChoices.FIRST_TERM)

    def test_semester_name_choices(self):
        for choice in Semester.SemesterChoices.choices:
            semester = Semester.objects.create(name=choice[0])
            self.assertEqual(semester.name, choice[0])
            semester.delete()

    def test_semester_name_invalid_choice(self):
        with self.assertRaises(ValidationError):
            Semester.objects.create(name="INVALID_CHOICE")

    def test_semester_default_values(self):
        semester = Semester.objects.create()
        self.assertEqual(semester.name, Semester.SemesterChoices.FIRST_TERM)
        self.assertEqual(semester.starts_at, date(2024, 9, 1))
        self.assertEqual(semester.ends_at, date(2024, 12, 31))

    def test_semester_id_is_uuid(self):
        semester = Semester.objects.create()
        self.assertIsNotNone(semester.id)
        self.assertTrue(isinstance(semester.id, UUID))

    def test_semester_created_at(self):
        semester = Semester.objects.create()
        self.assertIsNotNone(semester.created_at)
        self.assertIsInstance(semester.created_at, timezone.datetime)

    def test_semester_updated_at(self):
        semester = Semester.objects.create()
        first_updated_value = semester.updated_at
        self.assertIsNotNone(semester.updated_at)
        self.assertIsInstance(semester.updated_at, timezone.datetime)
        semester.name = Semester.SemesterChoices.SECOND_TERM
        semester.save()
        self.assertIsNotNone(semester.updated_at)
        self.assertGreater(semester.updated_at, first_updated_value)

    def test_starts_at_greater_than_ends_at(self):
        with self.assertRaises(ValueError):
            Semester.objects.create(
                starts_at=date(2024, 12, 31), ends_at=date(2024, 9, 1)
            )

    def test_multiple_current_semesters(self):
        today = timezone.now().date()
        semester1 = Semester(
            starts_at=today - timedelta(days=10), ends_at=today + timedelta(days=10)
        )
        semester1.save()
        with self.assertRaises(ValueError):
            semester2 = Semester(
                starts_at=today - timedelta(days=5), ends_at=today + timedelta(days=5)
            )
            semester2.save()


class CurrentSemesterManagerTestCase(TestCase):
    def test_get_current_semester(self):
        today = timezone.now().date()
        current_semester = Semester.objects.create(
            name=Semester.SemesterChoices.SECOND_TERM,
            starts_at=today - timedelta(days=9),
            ends_at=today + timedelta(days=80),
        )
        self.assertEqual(Semester.current.first(), current_semester)

    def test_current_semester_queryset(self):
        today = timezone.now().date()
        past_semester = Semester.objects.create(
            name=Semester.SemesterChoices.FIRST_TERM,
            starts_at=today - timedelta(days=100),
            ends_at=today - timedelta(days=10),
        )
        current_semester = Semester.objects.create(
            name=Semester.SemesterChoices.SECOND_TERM,
            starts_at=today - timedelta(days=9),
            ends_at=today + timedelta(days=80),
        )
        future_semester = Semester.objects.create(
            name=Semester.SemesterChoices.SUMMER_COURSE,
            starts_at=today + timedelta(days=81),
            ends_at=today + timedelta(days=170),
        )
        current_semesters = Semester.current.all()
        self.assertEqual(current_semesters.count(), 1)
        self.assertIn(current_semester, current_semesters)
        self.assertNotIn(past_semester, current_semesters)
        self.assertNotIn(future_semester, current_semesters)

    def test_no_current_semester(self):
        Semester.objects.all().delete()
        self.assertIsNone(Semester.current.first())
