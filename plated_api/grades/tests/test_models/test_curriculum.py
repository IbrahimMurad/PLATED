from datetime import date, datetime
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.test import TestCase
from grades.models import Curriculum, Path, Semester


class CurriculumTestCase(TestCase):
    def test_curriculum_with_valid_values(self) -> None:
        c: Curriculum = Curriculum.objects.create(
            name="Egyptian national curriculum", type="NATIONAL"
        )
        self.assertEqual(c.name, "Egyptian national curriculum")
        self.assertEqual(c.type, "NATIONAL")
        self.assertEqual(str(c), "Egyptian national curriculum")
        self.assertEqual(repr(c), "<Curriculum: Egyptian national curriculum>")

    def test_curriculum_with_invalide_type_choice(self) -> None:

        # test with using the label (display value) of the choice
        # this should include other invalid values, e.g. "NATIONALS" or "LOCAL"
        with self.assertRaises(ValidationError):
            Curriculum.objects.create(
                name="Egyptian national curriculum", type="National"
            )
        # test with empty string
        with self.assertRaises(ValidationError):
            Curriculum.objects.create(name="Egyptian national curriculum", type="")

    def test_display_value_of_curriculum_type(self) -> None:
        c: Curriculum = Curriculum.objects.create(
            name="Egyptian national curriculum", type="NATIONAL"
        )
        self.assertEqual(c.type, "NATIONAL")
        self.assertEqual(c.get_type_display(), "National")

    def test_curriculum_name_is_required(self) -> None:
        with self.assertRaises(ValidationError):
            Curriculum.objects.create()

    def test_curriculum_type_is_required(self) -> None:
        with self.assertRaises(ValidationError):
            Curriculum.objects.create(
                name="Egyptian national curriculum", type=None
            )  # type: ignore

    def test_curriculum_type_default(self) -> None:
        # not passing a type
        c: Curriculum = Curriculum.objects.create(name="Egyptian national curriculum")
        self.assertEqual(c.type, "NATIONAL")
        self.assertEqual(c.get_type_display(), "National")

    def test_curriculum_name_is_unique(self) -> None:
        Curriculum.objects.create(name="Egyptian national curriculum")
        with self.assertRaises(ValidationError):
            Curriculum.objects.create(name="Egyptian national curriculum")

    def test_curriculum_id_is_uuid(self) -> None:
        c: Curriculum = Curriculum.objects.create(name="Egyptian national curriculum")
        self.assertIsNotNone(c.id)
        self.assertTrue(isinstance(c.id, UUID))

    def test_curriculum_created_at(self) -> None:
        c: Curriculum = Curriculum.objects.create(name="Egyptian national curriculum")
        self.assertIsNotNone(c.created_at)
        self.assertIsInstance(c.created_at, datetime)

    def test_curriculum_updated_at(self) -> None:
        c: Curriculum = Curriculum.objects.create(name="Egyptian national curriculum")
        first_updated_value = c.updated_at
        self.assertIsNotNone(c.updated_at)
        self.assertIsInstance(c.updated_at, datetime)
        c.name = "Egyptian national curriculum updated"
        c.save()
        self.assertIsNotNone(c.updated_at)
        self.assertNotEqual(first_updated_value, c.updated_at)

    def test_curriculum_get_by_name(self) -> None:
        c: Curriculum = Curriculum.objects.create(name="Egyption national curriculum")
        self.assertEqual(
            Curriculum.objects.get(name="Egyption national curriculum"),
            c,
        )


class CurriculumPathRelationTestCase(TestCase):
    def test_curriculum_path_relation(self) -> None:
        c: Curriculum = Curriculum.objects.create(name="Egyptian national curriculum")
        p1: Path = Path.objects.create(
            name="Arabic path", curriculum=c, main_language="ARABIC"
        )
        p2: Path = Path.objects.create(
            name="English path", curriculum=c, main_language="ENGLISH"
        )
        self.assertEqual(c.paths.count(), 2)
        self.assertIn(p1, c.paths.all())
        self.assertIn(p2, c.paths.all())
        self.assertEqual(p1.curriculum, c)
        self.assertEqual(p2.curriculum, c)
        self.assertEqual(c.paths.get(name="Arabic path"), p1)
        self.assertEqual(c.paths.get(name="English path"), p2)

    def test_create_paths_from_curriculum(self) -> None:
        c: Curriculum = Curriculum.objects.create(name="Egyptian national curriculum")
        p1: Path = c.paths.create(name="Arabic path", main_language="ARABIC")
        p2: Path = c.paths.create(name="English path", main_language="ENGLISH")
        self.assertEqual(c.paths.count(), 2)
        self.assertIn(p1, c.paths.all())
        self.assertIn(p2, c.paths.all())
        self.assertEqual(p1.curriculum, c)
        self.assertEqual(p2.curriculum, c)

    def test_delete_curriculum_with_paths(self) -> None:
        c: Curriculum = Curriculum.objects.create(name="Egyptian national curriculum")
        c.paths.create(name="Arabic path", main_language="ARABIC")
        c.paths.create(name="English path", main_language="ENGLISH")
        self.assertEqual(c.paths.count(), 2)
        c.delete()
        self.assertEqual(Curriculum.objects.count(), 0)
        self.assertEqual(Path.objects.count(), 0)

    def test_get_curriculum_according_to_value_in_path(self) -> None:
        c_1: Curriculum = Curriculum.objects.create(name="Egyptian national curriculum")
        c_2: Curriculum = Curriculum.objects.create(name="IGCSE curriculum")
        c_1.paths.create(name="Arabic path", main_language="ARABIC")
        c_1.paths.create(name="English path", main_language="ENGLISH")
        c_2.paths.create(name="Math path", main_language="ENGLISH")
        queryset1: QuerySet = Curriculum.objects.filter(path__main_language="ENGLISH")
        self.assertEqual(queryset1.count(), 2)
        self.assertIn(c_1, queryset1)
        self.assertIn(c_2, queryset1)
        queryset2: QuerySet = Curriculum.objects.filter(path__name="Arabic path")
        self.assertEqual(queryset2.count(), 1)
        self.assertIn(c_1, queryset2)
        self.assertNotIn(c_2, queryset2)


class CurriculumSemesterRelationTestCase(TestCase):
    def setUp(self) -> None:
        self.curriculum: Curriculum = Curriculum.objects.create(
            name="Egyption National Curriculum"
        )
        self.s1: Semester = Semester.objects.create(curriculum=self.curriculum)
        self.s2: Semester = Semester.objects.create(
            curriculum=self.curriculum,
            starts_at=date(2025, 2, 1),
            ends_at=date(2025, 5, 31),
        )

    def test_curriculum_semester_relation(self) -> None:
        self.assertEqual(self.curriculum.semesters.count(), 2)
        self.assertIn(self.s1, self.curriculum.semesters.all())
        self.assertIn(self.s2, self.curriculum.semesters.all())
        self.assertEqual(self.s1.curriculum, self.curriculum)
        self.assertEqual(self.s2.curriculum, self.curriculum)
        self.assertEqual(
            self.curriculum.semesters.get(starts_at__lt=date(2025, 1, 1)), self.s1
        )
        self.assertEqual(
            self.curriculum.semesters.get(starts_at__gt=date(2025, 1, 1)), self.s2
        )

    def test_create_paths_from_curriculum(self) -> None:
        c: Curriculum = Curriculum.objects.create(name="IGCSE", type="INTERNATIONAL")
        s1: Semester = c.semesters.create(
            name="FIRST_TERM", starts_at=date(2024, 1, 1), ends_at=date(2024, 5, 31)
        )
        s2: Semester = c.semesters.create(
            name="SECOND_TERM", starts_at=date(2024, 6, 1), ends_at=date(2024, 12, 31)
        )
        self.assertEqual(c.semesters.count(), 2)
        self.assertIn(s1, c.semesters.all())
        self.assertIn(s2, c.semesters.all())
        self.assertEqual(s1.curriculum, c)
        self.assertEqual(s2.curriculum, c)

    def test_delete_curriculum_with_semester(self) -> None:
        self.assertEqual(self.curriculum.semesters.count(), 2)
        self.curriculum.delete()
        self.assertEqual(Curriculum.objects.count(), 0)
        self.assertEqual(Semester.objects.count(), 0)

    def test_get_curriculum_according_to_value_in_semester(self) -> None:
        c_1: Curriculum = Curriculum.objects.create(name="Egyptian national curriculum")
        c_2: Curriculum = Curriculum.objects.create(name="IGCSE curriculum")
        c_1.semesters.create(
            name="FIRST_TERM", starts_at=date(2024, 9, 1), ends_at=date(2025, 1, 31)
        )
        c_1.semesters.create(
            name="SECOND_TERM", starts_at=date(2025, 2, 1), ends_at=date(2025, 5, 31)
        )
        c_2.semesters.create(
            name="SUMMER_COURSE", starts_at=date(2025, 6, 1), ends_at=date(2025, 7, 31)
        )
        queryset1: QuerySet = Curriculum.objects.filter(semester__name="FIRST_TERM")
        self.assertEqual(queryset1.count(), 3)
        self.assertIn(c_1, queryset1)
        self.assertNotIn(c_2, queryset1)
        queryset2: QuerySet = Curriculum.objects.filter(semester__name="SUMMER_COURSE")
        self.assertEqual(queryset2.count(), 1)
        self.assertNotIn(c_1, queryset2)
        self.assertIn(c_2, queryset2)
