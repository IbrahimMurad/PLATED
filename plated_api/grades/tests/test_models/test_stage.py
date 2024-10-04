from datetime import datetime
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.test import TestCase
from grades.models import Curriculum, Path, Stage


class StageTestCase(TestCase):
    def setUp(self) -> None:
        self.curriculum: Curriculum = Curriculum.objects.create(
            name="Egyptian national curriculum"
        )
        self.path: Path = Path.objects.create(
            name="Arabic path", curriculum=self.curriculum
        )

    def test_stage_with_valid_values(self) -> None:
        stage: Stage = Stage.objects.create(
            name="Primary Stage", path=self.path, order_in_path=1
        )
        self.assertEqual(stage.name, "Primary Stage")
        self.assertEqual(stage.path, self.path)
        self.assertEqual(stage.order_in_path, 1)
        self.assertEqual(
            str(stage), "Primary Stage - Egyptian national curriculum - Arabic path"
        )
        self.assertEqual(
            repr(stage),
            "<Stage: Primary Stage - Egyptian national curriculum - Arabic path>",
        )

    def test_stage_name_is_required(self) -> None:
        with self.assertRaises(ValidationError):
            Stage.objects.create(path=self.path, order_in_path=1)

    def test_stage_path_is_required(self) -> None:
        with self.assertRaises(ValidationError):
            Stage.objects.create(name="Primary Stage", order_in_path=1)

    def test_stage_order_in_path_is_required(self) -> None:
        with self.assertRaises(ValidationError):
            Stage.objects.create(name="Primary Stage", path=self.path)

    def test_stage_id_is_uuid(self) -> None:
        stage: Stage = Stage.objects.create(
            name="Primary Stage", path=self.path, order_in_path=1
        )
        self.assertIsNotNone(stage.id)
        self.assertTrue(isinstance(stage.id, UUID))

    def test_stage_created_at(self) -> None:
        stage: Stage = Stage.objects.create(
            name="Primary Stage", path=self.path, order_in_path=1
        )
        self.assertIsNotNone(stage.created_at)
        self.assertIsInstance(stage.created_at, datetime)

    def test_stage_updated_at(self) -> None:
        stage: Stage = Stage.objects.create(
            name="Primary Stage", path=self.path, order_in_path=1
        )
        first_updated_value: datetime = stage.updated_at
        self.assertIsNotNone(stage.updated_at)
        self.assertIsInstance(stage.updated_at, datetime)
        stage.name = "Primary Stage Updated"
        stage.save()
        self.assertIsNotNone(stage.updated_at)
        self.assertGreater(stage.updated_at, first_updated_value)

    def test_stage_get_by_name(self) -> None:
        stage: Stage = Stage.objects.create(
            name="Primary Stage", path=self.path, order_in_path=1
        )
        self.assertEqual(Stage.objects.filter(name="Primary Stage")[0], stage)

    def test_stage_ordering(self) -> None:
        stage1: Stage = Stage.objects.create(
            name="Secondary Stage", path=self.path, order_in_path=2
        )
        stage2: Stage = Stage.objects.create(
            name="Primary Stage", path=self.path, order_in_path=1
        )
        stages: QuerySet = Stage.objects.all()
        self.assertEqual(stages[0], stage2)
        self.assertEqual(stages[1], stage1)


class StagePathRelationTestCase(TestCase):
    def setUp(self) -> None:
        self.curriculum: Curriculum = Curriculum.objects.create(
            name="Egyptian national curriculum"
        )
        self.path: Path = Path.objects.create(
            name="Arabic path", curriculum=self.curriculum
        )

    def test_stage_path_is_Path_instance(self) -> None:
        stage: Stage = Stage.objects.create(
            name="Primary Stage", path=self.path, order_in_path=1
        )
        self.assertEqual(stage.path, self.path)
        self.assertTrue(isinstance(stage.path, Path))

    def test_stage_path_is_deleted(self) -> None:
        Stage.objects.create(name="Primary Stage", path=self.path, order_in_path=1)
        self.path.delete()
        with self.assertRaises(Stage.DoesNotExist):
            Stage.objects.get(name="Primary Stage")

    def test_stage_path_is_updated(self) -> None:
        stage: Stage = Stage.objects.create(
            name="Primary Stage", path=self.path, order_in_path=1
        )
        self.path.name = "Arabic path updated"
        self.path.save()
        stage.refresh_from_db()
        self.assertEqual(stage.path.name, "Arabic path updated")

    def test_stage_path_is_updated_with_new_instance(self) -> None:
        new_path: Path = Path.objects.create(
            name="English path", curriculum=self.curriculum
        )
        stage: Stage = Stage.objects.create(
            name="Primary Stage", path=self.path, order_in_path=1
        )
        stage.path = new_path
        stage.save()
        stage.refresh_from_db()
        self.assertEqual(stage.path.name, "English path")

    def test_get_stage_by_path(self) -> None:
        stage1: Stage = Stage.objects.create(
            name="Primary Stage", path=self.path, order_in_path=1
        )
        stage2: Stage = Stage.objects.create(
            name="Secondary Stage", path=self.path, order_in_path=2
        )
        queryset: QuerySet = Stage.objects.filter(path=self.path)
        self.assertEqual(queryset.count(), 2)
        self.assertIn(stage1, queryset)
        self.assertIn(stage2, queryset)

    def test_get_stage_by_path_name(self) -> None:
        stage1: Stage = Stage.objects.create(
            name="Primary Stage", path=self.path, order_in_path=1
        )
        stage2: Stage = Stage.objects.create(
            name="Secondary Stage", path=self.path, order_in_path=2
        )
        queryset: QuerySet = Stage.objects.filter(path__name="Arabic path")
        self.assertEqual(queryset.count(), 2)
        self.assertIn(stage1, queryset)
        self.assertIn(stage2, queryset)

    def test_get_stage_by_curriculum(self) -> None:
        stage1: Stage = Stage.objects.create(
            name="Primary Stage", path=self.path, order_in_path=1
        )
        stage2: Stage = Stage.objects.create(
            name="Secondary Stage", path=self.path, order_in_path=2
        )
        queryset: QuerySet = Stage.objects.filter(path__curriculum=self.curriculum)
        self.assertEqual(queryset.count(), 2)
        self.assertIn(stage1, queryset)
        self.assertIn(stage2, queryset)

    def test_stage_curriculum_is_deleted(self) -> None:
        Stage.objects.create(name="Primary Stage", path=self.path, order_in_path=1)
        self.curriculum.delete()
        with self.assertRaises(Stage.DoesNotExist):
            Stage.objects.get(name="Primary Stage")
