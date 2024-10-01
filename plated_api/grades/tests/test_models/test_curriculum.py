from datetime import datetime
from uuid import UUID

from django.core.exceptions import ValidationError
from django.test import TestCase
from grades.models import Curriculum, Path


class CurriculumTestCase(TestCase):
    def test_curriculum_with_valid_values(self):
        c = Curriculum.objects.create(
            name="Egyptian national curriculum", type="NATIONAL"
        )
        self.assertEqual(c.name, "Egyptian national curriculum")
        self.assertEqual(c.type, "NATIONAL")
        self.assertEqual(str(c), "Egyptian national curriculum")
        self.assertEqual(repr(c), "<Curriculum: Egyptian national curriculum>")

    def test_curriculum_with_invalide_type_choice(self):

        # test with using the label (display value) of the choice
        # this should include other invalid values, e.g. "NATIONALS" or "LOCAL"
        with self.assertRaises(ValidationError):
            Curriculum.objects.create(
                name="Egyptian national curriculum", type="National"
            )
        # test with empty string
        with self.assertRaises(ValidationError):
            Curriculum.objects.create(name="Egyptian national curriculum", type="")

    def test_display_value_of_curriculum_type(self):
        c = Curriculum.objects.create(
            name="Egyptian national curriculum", type="NATIONAL"
        )
        self.assertEqual(c.type, "NATIONAL")
        self.assertEqual(c.get_type_display(), "National")

    def test_curriculum_name_is_required(self):
        with self.assertRaises(ValidationError):
            Curriculum.objects.create()

    def test_curriculum_type_is_required(self):
        with self.assertRaises(ValidationError):
            Curriculum.objects.create(name="Egyptian national curriculum", type=None)

    def test_curriculum_type_default(self):
        # not passing a type
        c = Curriculum.objects.create(name="Egyptian national curriculum")
        self.assertEqual(c.type, "NATIONAL")
        self.assertEqual(c.get_type_display(), "National")

    def test_curriculum_name_is_unique(self):
        Curriculum.objects.create(name="Egyptian national curriculum")
        with self.assertRaises(ValidationError):
            Curriculum.objects.create(name="Egyptian national curriculum")

    def test_curriculum_id_is_uuid(self):
        c = Curriculum.objects.create(name="Egyptian national curriculum")
        self.assertIsNotNone(c.id)
        self.assertTrue(isinstance(c.id, UUID))

    def test_curriculum_created_at(self):
        c = Curriculum.objects.create(name="Egyptian national curriculum")
        self.assertIsNotNone(c.created_at)
        self.assertIsInstance(c.created_at, datetime)

    def test_curriculum_updated_at(self):
        c = Curriculum.objects.create(name="Egyptian national curriculum")
        first_updated_value = c.updated_at
        self.assertIsNotNone(c.updated_at)
        self.assertIsInstance(c.updated_at, datetime)
        c.name = "Egyptian national curriculum updated"
        c.save()
        self.assertIsNotNone(c.updated_at)
        self.assertNotEqual(first_updated_value, c.updated_at)

    def test_curriculum_get_by_name(self):
        c = Curriculum.objects.create(name="Egyption national curriculum")
        self.assertEqual(
            Curriculum.objects.get(name="Egyption national curriculum"),
            c,
        )


class CurriculumPathRelationTestCase(TestCase):
    def test_curriculum_path_relation(self):
        c = Curriculum.objects.create(name="Egyptian national curriculum")
        p1 = Path.objects.create(
            name="Arabic path", curriculum=c, main_language="ARABIC"
        )
        p2 = Path.objects.create(
            name="English path", curriculum=c, main_language="ENGLISH"
        )
        self.assertEqual(c.paths.count(), 2)
        self.assertIn(p1, c.paths.all())
        self.assertIn(p2, c.paths.all())
        self.assertEqual(p1.curriculum, c)
        self.assertEqual(p2.curriculum, c)
        self.assertEqual(c.paths.get(name="Arabic path"), p1)
        self.assertEqual(c.paths.get(name="English path"), p2)

    def test_create_paths_from_curriculum(self):
        c = Curriculum.objects.create(name="Egyptian national curriculum")
        p1 = c.paths.create(name="Arabic path", main_language="ARABIC")
        p2 = c.paths.create(name="English path", main_language="ENGLISH")
        self.assertEqual(c.paths.count(), 2)
        self.assertIn(p1, c.paths.all())
        self.assertIn(p2, c.paths.all())
        self.assertEqual(p1.curriculum, c)
        self.assertEqual(p2.curriculum, c)

    def test_delete_curriculum_with_paths(self):
        c = Curriculum.objects.create(name="Egyptian national curriculum")
        c.paths.create(name="Arabic path", main_language="ARABIC")
        c.paths.create(name="English path", main_language="ENGLISH")
        self.assertEqual(c.paths.count(), 2)
        c.delete()
        self.assertEqual(Curriculum.objects.count(), 0)
        self.assertEqual(Path.objects.count(), 0)

    def test_get_curriculum_according_to_value_in_path(self):
        c_1 = Curriculum.objects.create(name="Egyptian national curriculum")
        c_2 = Curriculum.objects.create(name="IGCSE curriculum")
        c_1.paths.create(name="Arabic path", main_language="ARABIC")
        c_1.paths.create(name="English path", main_language="ENGLISH")
        c_2.paths.create(name="Math path", main_language="ENGLISH")
        queryset1 = Curriculum.objects.filter(path__main_language="ENGLISH")
        self.assertEqual(queryset1.count(), 2)
        self.assertIn(c_1, queryset1)
        self.assertIn(c_2, queryset1)
        queryset2 = Curriculum.objects.filter(path__name="Arabic path")
        self.assertEqual(queryset2.count(), 1)
        self.assertIn(c_1, queryset2)
        self.assertNotIn(c_2, queryset2)
