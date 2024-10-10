from datetime import datetime
from uuid import UUID

from django.core.exceptions import ValidationError
from django.test import TestCase
from questions.models import Type
from resources.models import Subject


class TypeTestCase(TestCase):
    def setUp(self) -> None:
        self.physics = Subject.objects.create(name="Physics")
        self.single_step_question = Type.objects.create(
            subject=self.physics,
            name="Single-Step question",
            description="A question that can be answered in one step.",
        )
        self.multi_steps_question = Type.objects.create(
            subject=self.physics,
            name="Multi-Steps question",
            description="A question that requires multiple steps.",
        )
        self.qualitative = Type.objects.create(
            subject=self.physics,
            name="Qualitative",
            description=(
                "Requires reasoning or logical analysis"
                "without relying on calculations."
            ),
        )
        self.quantitative = Type.objects.create(
            subject=self.physics,
            name="Quantitative",
            description="Involves calculations, often numerical, to solve the problem.",
        )
        self.conceptual = Type.objects.create(
            subject=self.physics,
            name="Conceptual",
            description=(
                "Focuses on understanding of theories and principles"
                "without requiring heavy calculations."
            ),
        )
        self.computational = Type.objects.create(
            subject=self.physics,
            name="Computational",
            description=(
                "Requires mathematical computation,"
                "often involving formulas and numerical answers."
            ),
        )

    def test_type_creation(self) -> None:
        self.assertEqual(self.single_step_question.name, "Single-Step question")
        self.assertEqual(self.multi_steps_question.name, "Multi-Steps question")
        self.assertEqual(self.conceptual.name, "Conceptual")
        self.assertEqual(self.computational.name, "Computational")
        self.assertEqual(self.qualitative.name, "Qualitative")
        self.assertEqual(self.quantitative.name, "Quantitative")

    def test_ordering(self) -> None:
        self.assertEqual(
            list(Type.objects.all()),
            [
                self.computational,
                self.conceptual,
                self.multi_steps_question,
                self.qualitative,
                self.quantitative,
                self.single_step_question,
            ],
        )

    def test_id_is_uuid(self) -> None:
        self.assertIsNotNone(self.conceptual.id)
        self.assertIsInstance(self.conceptual.id, UUID)

    def test_create_at_is_datetime(self) -> None:
        self.assertIsNotNone(self.qualitative.created_at)
        self.assertIsInstance(self.qualitative.created_at, datetime)

    def test_updated_at_is_datetime(self) -> None:
        self.assertIsNotNone(self.single_step_question.updated_at)
        self.assertIsInstance(self.single_step_question.updated_at, datetime)

    def test_updated_at_is_updated_after_updating(self) -> None:
        old_datetime: datetime = self.multi_steps_question.updated_at
        self.multi_steps_question.name = "Multiple steps"
        self.multi_steps_question.save()
        self.assertGreater(self.multi_steps_question.updated_at, old_datetime)

    def test_name_is_required(self) -> None:
        with self.assertRaises(ValidationError):
            Type.objects.create(subject=self.physics)

    def test_subject_is_optional(self) -> None:
        no_subject_type: Type = Type.objects.create(name="Type with no subject")
        self.assertEqual(no_subject_type.name, "Type with no subject")
        self.assertIsNotNone(no_subject_type.id)

    def test_get_all_types_from_subject(self) -> None:
        self.assertEqual(
            list(self.physics.types.all()),
            [
                self.computational,
                self.conceptual,
                self.multi_steps_question,
                self.qualitative,
                self.quantitative,
                self.single_step_question,
            ],
        )

    def test_update_type(self):
        # Test updating a type
        self.conceptual.name = "True/False"
        self.conceptual.description = "A question with only two possible answers."
        self.conceptual.save()

        # Refresh from database
        self.conceptual.refresh_from_db()

        self.assertEqual(self.conceptual.name, "True/False")
        self.assertEqual(
            self.conceptual.description, "A question with only two possible answers."
        )

    def test_cascade_delete_subject(self):
        # Test that deleting a subject cascades to its types and questions
        subject_id = self.physics.id
        self.physics.delete()

        # Check that the type no longer exists
        with self.assertRaises(Type.DoesNotExist):
            Type.objects.get(id=self.single_step_question.id)

        # Check that the subject no longer exists
        with self.assertRaises(Subject.DoesNotExist):
            Subject.objects.get(id=subject_id)
