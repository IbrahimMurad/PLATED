from datetime import datetime
from uuid import UUID

from django.core.exceptions import ValidationError
from django.test import TestCase
from grades.models import Curriculum, Path


class PathTestCase(TestCase):
    def test_Path_with_valid_values(self):
        c = Curriculum.objects.create(name="Egyptian national curriculum")
        p = Path.objects.create(
            name="Arabic path", main_language="ARABIC", curriculum=c
        )
        self.assertEqual(p.name, "Arabic path")
        self.assertEqual(p.main_language, "ARABIC")
        self.assertEqual(str(p), "Egyptian national curriculum - Arabic path")
        self.assertEqual(repr(p), "<Path: Egyptian national curriculum - Arabic path>")

    def test_Path_with_invalide_language_choice(self):

        c = Curriculum.objects.create(name="Egyptian national curriculum")
        # test with using the label (display value) of the choice
        # this should include other invalid values, e.g. "french" or "عربي"
        with self.assertRaises(ValidationError):
            Path.objects.create(
                name="Arabic path", main_language="Arabic", curriculum=c
            )
        # test with empty string
        with self.assertRaises(ValidationError):
            Path.objects.create(name="Arabic path", main_language="", curriculum=c)

    def test_display_value_of_Path_type(self):
        c = Curriculum.objects.create(name="Egyptian national curriculum")
        p = Path.objects.create(
            name="Arabic path", curriculum=c, main_language="ARABIC"
        )
        self.assertEqual(p.main_language, "ARABIC")
        self.assertEqual(p.get_main_language_display(), "Arabic")

    def test_Path_name_is_required(self):
        c = Curriculum.objects.create(name="Egyptian national curriculum")
        with self.assertRaises(ValidationError):
            Path.objects.create(curriculum=c)

    def test_Path_curriculum_is_required(self):
        with self.assertRaises(ValidationError):
            Path.objects.create(name="Arabic path")

    def test_Path_main_language_is_required(self):
        with self.assertRaises(ValidationError):
            c = Curriculum.objects.create(name="Egyptian national curriculum")
            Path.objects.create(
                name="Egyptian national Path", curriculum=c, main_language=None
            )

    def test_Path_language_default(self):
        # not passing a type
        c = Curriculum.objects.create(name="Egyptian national curriculum")
        p = Path.objects.create(name="Arabic path", curriculum=c)
        self.assertEqual(p.main_language, "ENGLISH")
        self.assertEqual(p.get_main_language_display(), "English")

    def test_Path_id_is_uuid(self):
        c = Curriculum.objects.create(name="Egyptian national curriculum")
        p = Path.objects.create(name="Arabic path", curriculum=c)
        self.assertIsNotNone(p.id)
        self.assertTrue(isinstance(p.id, UUID))

    def test_Path_created_at(self):
        c = Curriculum.objects.create(name="Egyptian national curriculum")
        p = Path.objects.create(name="Arabic path", curriculum=c)
        self.assertIsNotNone(p.created_at)
        self.assertIsInstance(p.created_at, datetime)

    def test_Path_updated_at(self):
        c = Curriculum.objects.create(name="Egyptian national curriculum")
        p = Path.objects.create(name="Arabic path", curriculum=c)
        first_updated_value = p.updated_at
        self.assertIsNotNone(p.updated_at)
        self.assertIsInstance(p.updated_at, datetime)
        p.name = "Arabic path updated"
        p.save()
        self.assertIsNotNone(p.updated_at)
        self.assertGreater(p.updated_at, first_updated_value)

    def test_Path_get_by_name(self):
        c = Curriculum.objects.create(name="Egyptian national curriculum")
        p = Path.objects.create(name="Arabic path", curriculum=c)
        self.assertEqual(Path.objects.get(name="Arabic path"), p)


class PathCurriculumRelationTestCase(TestCase):

    def test_path_curriculum_is_Curriculum_instance(self):
        c = Curriculum.objects.create(name="Egyptian national curriculum")
        p = Path.objects.create(name="Arabic path", curriculum=c)
        self.assertEqual(p.curriculum, c)
        self.assertTrue(isinstance(p.curriculum, Curriculum))

    def test_path_curriculum_is_required(self):
        with self.assertRaises(ValidationError):
            Path.objects.create(name="Arabic path", curriculum=None)

    def test_path_curriculum_is_deleted(self):
        c = Curriculum.objects.create(name="Egyptian national curriculum")
        Path.objects.create(name="Arabic path", curriculum=c)
        c.delete()
        with self.assertRaises(Path.DoesNotExist):
            Path.objects.get(name="Arabic path")

    def test_path_curriculum_is_updated(self):
        c = Curriculum.objects.create(name="Egyptian national curriculum")
        p = Path.objects.create(name="Arabic path", curriculum=c)
        c.name = "Egyptian national curriculum updated"
        c.save()
        p.refresh_from_db()
        self.assertEqual(p.curriculum.name, "Egyptian national curriculum updated")

    def test_path_curriculum_is_updated_with_new_instance(self):
        c1 = Curriculum.objects.create(name="Egyptian national curriculum")
        c2 = Curriculum.objects.create(name="IGCSE curriculum")
        p = Path.objects.create(name="Arabic path", curriculum=c1)
        p.curriculum = c2
        p.save()
        p.refresh_from_db()
        self.assertEqual(p.curriculum.name, "IGCSE curriculum")

    def test_get_path_by_curriculum(self):
        c = Curriculum.objects.create(name="Egyptian national curriculum")
        p1 = Path.objects.create(
            name="Arabic path", curriculum=c, main_language="ARABIC"
        )
        p2 = Path.objects.create(name="English path", curriculum=c)
        queryset = Path.objects.filter(curriculum=c)
        self.assertEqual(queryset.count(), 2)
        self.assertIn(p1, queryset)
        self.assertIn(p2, queryset)

    def test_get_path_by_curriculum_name(self):
        c = Curriculum.objects.create(name="Egyptian national curriculum")
        p1 = Path.objects.create(
            name="Arabic path", curriculum=c, main_language="ARABIC"
        )
        p2 = Path.objects.create(name="English path", curriculum=c)
        queryset = Path.objects.filter(curriculum__name="Egyptian national curriculum")
        self.assertEqual(queryset.count(), 2)
        self.assertIn(p1, queryset)
        self.assertIn(p2, queryset)
