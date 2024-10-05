from datetime import datetime
from uuid import UUID

from django.core.exceptions import ValidationError
from django.db.models import QuerySet
from django.test import TestCase
from grades.models import Curriculum, Grade, Path, Stage


class GradeTestCase(TestCase):
    def setUp(self) -> None:
        self.curriculum: Curriculum = Curriculum.objects.create(
            name="Egyptian national curriculum"
        )
        self.path: Path = Path.objects.create(
            name="Arabic path", curriculum=self.curriculum
        )
        self.stage: Stage = Stage.objects.create(
            name="Primary Stage", path=self.path, order_in_path=1
        )

    def test_grade_with_valid_values(self) -> None:
        grade: Grade = Grade.objects.create(
            name="First Grade", stage=self.stage, order_in_stage=1
        )
        self.assertEqual(grade.name, "First Grade")
        self.assertEqual(grade.stage, self.stage)
        self.assertEqual(grade.order_in_stage, 1)
        self.assertEqual(
            str(grade),
            "First Grade - Primary Stage - Egyptian national curriculum - Arabic path",
        )
        self.assertEqual(
            repr(grade),
            "<Grade: First Grade - Primary Stage "
            + "- Egyptian national curriculum - Arabic path>",
        )

    def test_grade_name_is_required(self) -> None:
        with self.assertRaises(ValidationError):
            Grade.objects.create(stage=self.stage, order_in_stage=1)

    def test_grade_stage_is_required(self) -> None:
        with self.assertRaises(ValidationError):
            Grade.objects.create(name="First Grade", order_in_stage=1)

    def test_grade_order_in_stage_is_required(self) -> None:
        with self.assertRaises(ValidationError):
            Grade.objects.create(name="First Grade", stage=self.stage)

    def test_grade_id_is_uuid(self) -> None:
        grade: Grade = Grade.objects.create(
            name="First Grade", stage=self.stage, order_in_stage=1
        )
        self.assertIsNotNone(grade.id)
        self.assertIsInstance(grade.id, UUID)

    def test_grade_created_at(self) -> None:
        grade: Grade = Grade.objects.create(
            name="First Grade", stage=self.stage, order_in_stage=1
        )
        self.assertIsNotNone(grade.created_at)
        self.assertIsInstance(grade.created_at, datetime)

    def test_grade_updated_at(self) -> None:
        grade: Grade = Grade.objects.create(
            name="First Grade", stage=self.stage, order_in_stage=1
        )
        first_updated_value: datetime = grade.updated_at
        self.assertIsNotNone(grade.updated_at)
        self.assertIsInstance(grade.updated_at, datetime)
        grade.name = "First Grade Updated"
        grade.save()
        self.assertIsNotNone(grade.updated_at)
        self.assertGreater(grade.updated_at, first_updated_value)

    def test_grade_filter_by_name(self) -> None:
        grade: Grade = Grade.objects.create(
            name="First Grade", stage=self.stage, order_in_stage=1
        )
        self.assertEqual(Grade.objects.filter(name="First Grade")[0], grade)

    def test_grade_ordering(self) -> None:
        grade1: Grade = Grade.objects.create(
            name="Second Grade", stage=self.stage, order_in_stage=2
        )
        grade2: Grade = Grade.objects.create(
            name="First Grade", stage=self.stage, order_in_stage=1
        )
        grades: QuerySet = Grade.objects.all()
        self.assertEqual(grades[0], grade2)
        self.assertEqual(grades[1], grade1)


class GradeStageRelationTestCase(TestCase):
    def setUp(self) -> None:
        self.curriculum: Curriculum = Curriculum.objects.create(
            name="Egyptian national curriculum"
        )
        self.path: Path = Path.objects.create(
            name="Arabic path", curriculum=self.curriculum
        )
        self.stage: Stage = Stage.objects.create(
            name="Primary Stage", path=self.path, order_in_path=1
        )

    def test_grade_stage_is_Stage_instance(self) -> None:
        grade: Grade = Grade.objects.create(
            name="First Grade", stage=self.stage, order_in_stage=1
        )
        self.assertEqual(grade.stage, self.stage)
        self.assertTrue(isinstance(grade.stage, Stage))

    def test_grade_stage_is_deleted(self) -> None:
        Grade.objects.create(name="First Grade", stage=self.stage, order_in_stage=1)
        self.stage.delete()
        with self.assertRaises(Grade.DoesNotExist):
            Grade.objects.get(name="First Grade")

    def test_grade_path_is_deleted(self) -> None:
        Grade.objects.create(name="First Grade", stage=self.stage, order_in_stage=1)
        self.path.delete()
        with self.assertRaises(Grade.DoesNotExist):
            Grade.objects.get(name="First Grade")

    def test_grade_curriculum_is_deleted(self) -> None:
        Grade.objects.create(name="First Grade", stage=self.stage, order_in_stage=1)
        self.curriculum.delete()
        with self.assertRaises(Grade.DoesNotExist):
            Grade.objects.get(name="First Grade")

    def test_grade_stage_is_updated(self) -> None:
        grade: Grade = Grade.objects.create(
            name="First Grade", stage=self.stage, order_in_stage=1
        )
        self.stage.name = "Primary Stage Updated"
        self.stage.save()
        grade.refresh_from_db()
        self.assertEqual(grade.stage.name, "Primary Stage Updated")

    def test_grade_stage_is_updated_with_new_instance(self) -> None:
        new_stage: Stage = Stage.objects.create(
            name="Secondary Stage", path=self.path, order_in_path=2
        )
        grade: Grade = Grade.objects.create(
            name="First Grade", stage=self.stage, order_in_stage=1
        )
        grade.stage = new_stage
        grade.save()
        grade.refresh_from_db()
        self.assertEqual(grade.stage.name, "Secondary Stage")

    def test_get_grade_by_stage(self) -> None:
        grade1: Grade = Grade.objects.create(
            name="First Grade", stage=self.stage, order_in_stage=1
        )
        grade2: Grade = Grade.objects.create(
            name="Second Grade", stage=self.stage, order_in_stage=2
        )
        queryset: QuerySet = Grade.objects.filter(stage=self.stage)
        self.assertEqual(queryset.count(), 2)
        self.assertIn(grade1, queryset)
        self.assertIn(grade2, queryset)

    def test_get_grade_by_stage_name(self) -> None:
        grade1: Grade = Grade.objects.create(
            name="First Grade", stage=self.stage, order_in_stage=1
        )
        grade2: Grade = Grade.objects.create(
            name="Second Grade", stage=self.stage, order_in_stage=2
        )
        queryset: QuerySet = Grade.objects.filter(stage__name="Primary Stage")
        self.assertEqual(queryset.count(), 2)
        self.assertIn(grade1, queryset)
        self.assertIn(grade2, queryset)

    def test_get_grade_by_path(self) -> None:
        grade1: Grade = Grade.objects.create(
            name="First Grade", stage=self.stage, order_in_stage=1
        )
        grade2: Grade = Grade.objects.create(
            name="Second Grade", stage=self.stage, order_in_stage=2
        )
        queryset: QuerySet = Grade.objects.filter(stage__path=self.path)
        self.assertEqual(queryset.count(), 2)
        self.assertIn(grade1, queryset)
        self.assertIn(grade2, queryset)

    def test_get_grade_by_curriculum(self) -> None:
        grade1: Grade = Grade.objects.create(
            name="First Grade", stage=self.stage, order_in_stage=1
        )
        grade2: Grade = Grade.objects.create(
            name="Second Grade", stage=self.stage, order_in_stage=2
        )
        queryset: QuerySet = Grade.objects.filter(
            stage__path__curriculum=self.curriculum
        )
        self.assertEqual(queryset.count(), 2)
        self.assertIn(grade1, queryset)
        self.assertIn(grade2, queryset)
