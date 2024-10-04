from datetime import date, datetime, timedelta
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.test import TestCase
from django.utils import timezone
from grades.models import Curriculum, Semester


class SemesterTestCase(TestCase):
    def setUp(self) -> None:
        self.curriculum: Curriculum = Curriculum.objects.create(
            name="Egyption National Curriculum"
        )

    def test_semester_with_valid_values(self) -> None:
        semester: Semester = Semester.objects.create(
            name=Semester.SemesterChoices.FIRST_TERM,
            starts_at=date(2024, 9, 1),
            ends_at=date(2024, 12, 31),
            curriculum=self.curriculum,
        )
        self.assertEqual(semester.name, Semester.SemesterChoices.FIRST_TERM)
        self.assertEqual(semester.starts_at, date(2024, 9, 1))
        self.assertEqual(semester.ends_at, date(2024, 12, 31))
        self.assertEqual(str(semester), Semester.SemesterChoices.FIRST_TERM)
        self.assertEqual(semester.curriculum, self.curriculum)

    def test_semester_name_choices(self) -> None:
        for choice in Semester.SemesterChoices.choices:
            semester: Semester = Semester.objects.create(name=choice[0])
            self.assertEqual(semester.name, choice[0])
            semester.delete()

    def test_semester_name_invalid_choice(self) -> None:
        with self.assertRaises(ValidationError):
            Semester.objects.create(name="INVALID_CHOICE")

    def test_semester_default_values(self) -> None:
        semester: Semester = Semester.objects.create()
        self.assertEqual(semester.name, Semester.SemesterChoices.FIRST_TERM)
        self.assertEqual(semester.starts_at, date(2024, 9, 1))
        self.assertEqual(semester.ends_at, date(2024, 12, 31))
        self.assertIsNone(semester.curriculum)

    def test_semester_id_is_uuid(self) -> None:
        semester: Semester = Semester.objects.create()
        self.assertIsNotNone(semester.id)
        self.assertTrue(isinstance(semester.id, UUID))

    def test_semester_created_at(self) -> None:
        semester = Semester.objects.create()
        self.assertIsNotNone(semester.created_at)
        self.assertIsInstance(semester.created_at, datetime)

    def test_semester_updated_at(self) -> None:
        semester = Semester.objects.create()
        first_updated_value: datetime = semester.updated_at
        self.assertIsNotNone(semester.updated_at)
        self.assertIsInstance(semester.updated_at, datetime)
        semester.name = Semester.SemesterChoices.SECOND_TERM.value
        semester.save()
        self.assertIsNotNone(semester.updated_at)
        self.assertGreater(semester.updated_at, first_updated_value)

    def test_starts_at_greater_than_ends_at(self) -> None:
        with self.assertRaises(ValueError):
            Semester.objects.create(
                starts_at=date(2024, 12, 31), ends_at=date(2024, 9, 1)
            )

    def test_multiple_current_semesters(self) -> None:
        today: date = timezone.now().date()
        semester1: Semester = Semester(
            starts_at=today - timedelta(days=10), ends_at=today + timedelta(days=10)
        )
        semester1.save()
        with self.assertRaises(ValueError):
            semester2: Semester = Semester(
                starts_at=today - timedelta(days=5), ends_at=today + timedelta(days=5)
            )
            semester2.save()


class CurrentSemesterManagerTestCase(TestCase):
    def setUp(self) -> None:
        self.curriculum: Curriculum = Curriculum.objects.create(
            name="Egyption National Curriculum"
        )

    def test_get_current_semester(self) -> None:
        today: date = timezone.now().date()
        current_semester: Semester = Semester.objects.create(
            name=Semester.SemesterChoices.SECOND_TERM,
            starts_at=today - timedelta(days=9),
            ends_at=today + timedelta(days=80),
            curriculum=self.curriculum,
        )
        self.assertEqual(
            Semester.current.filter(curriculum=self.curriculum).first(),
            current_semester,
        )

    def test_current_semester_queryset(self) -> None:
        today: date = timezone.now().date()
        past_semester: Semester = Semester.objects.create(
            name=Semester.SemesterChoices.FIRST_TERM,
            starts_at=today - timedelta(days=100),
            ends_at=today - timedelta(days=10),
            curriculum=self.curriculum,
        )
        current_semester: Semester = Semester.objects.create(
            name=Semester.SemesterChoices.SECOND_TERM,
            starts_at=today - timedelta(days=9),
            ends_at=today + timedelta(days=80),
            curriculum=self.curriculum,
        )
        future_semester: Semester = Semester.objects.create(
            name=Semester.SemesterChoices.SUMMER_COURSE,
            starts_at=today + timedelta(days=81),
            ends_at=today + timedelta(days=170),
            curriculum=self.curriculum,
        )
        current_semesters: QuerySet = Semester.current.filter(
            curriculum=self.curriculum
        )
        self.assertEqual(current_semesters.count(), 1)
        self.assertIn(current_semester, current_semesters)
        self.assertNotIn(past_semester, current_semesters)
        self.assertNotIn(future_semester, current_semesters)

    def test_no_current_semester(self) -> None:
        Semester.objects.all().delete()
        self.assertIsNone(Semester.current.first())


class SemesterCurriculumRelationTestCase(TestCase):
    def setUp(self) -> None:
        self.curriculum: Curriculum = Curriculum.objects.create(
            name="Egyption National Curriculum"
        )

    def test_semester_curriculum_is_Curriculum_instance(self) -> None:
        semester: Semester = Semester.objects.create(curriculum=self.curriculum)
        self.assertIsInstance(semester.curriculum, Curriculum)

    def test_semester_curriculum_is_deleted(self) -> None:
        Semester.objects.create(curriculum=self.curriculum)
        self.curriculum.delete()
        self.curriculum.save()
        with self.assertRaises(Semester.DoesNotExist):
            Semester.objects.get(curriculum=self.curriculum)

    def test_path_curriculum_is_updated(self) -> None:
        semester: Semester = Semester.objects.create(curriculum=self.curriculum)
        self.curriculum.name = "Egyptian national curriculum updated"
        self.curriculum.save()
        self.curriculum.refresh_from_db()
        self.assertEqual(
            semester.curriculum.name,  # type: ignore
            "Egyptian national curriculum updated",
        )

    def test_path_curriculum_is_updated_with_new_instance(self) -> None:
        semester: Semester = Semester.objects.create(curriculum=self.curriculum)
        new_curriculum: Curriculum = Curriculum.objects.create(
            name="IGCSE", type="INTERNATIONAL"
        )
        semester.curriculum = new_curriculum
        semester.save()
        self.assertEqual(semester.curriculum, new_curriculum)
        self.assertNotEqual(semester.curriculum, self.curriculum)

    def test_get_semester_by_curriculum(self) -> None:
        s1: Semester = Semester.objects.create(curriculum=self.curriculum)
        s2: Semester = Semester.objects.create(
            curriculum=self.curriculum,
            starts_at=date(2024, 2, 1),
            ends_at=date(2024, 5, 31),
        )
        queryset: QuerySet = Semester.objects.filter(curriculum=self.curriculum)
        self.assertEqual(queryset.count(), 2)
        self.assertIn(s1, queryset)
        self.assertIn(s2, queryset)

    def test_get_path_by_curriculum_name(self):
        s1: Semester = Semester.objects.create(curriculum=self.curriculum)
        s2: Semester = Semester.objects.create(
            curriculum=self.curriculum,
            starts_at=date(2024, 2, 1),
            ends_at=date(2024, 5, 31),
        )
        queryset: QuerySet = Semester.objects.filter(
            curriculum__name="Egyption National Curriculum"
        )
        self.assertEqual(queryset.count(), 2)
        self.assertIn(s1, queryset)
        self.assertIn(s2, queryset)
