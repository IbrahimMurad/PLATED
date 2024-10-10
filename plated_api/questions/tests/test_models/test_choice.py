from io import BytesIO
from uuid import UUID

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import QuerySet
from django.test import TestCase
from PIL import Image
from questions.models import Choice, Question, Type
from resources.models import Chapter, Lesson, Subject, TextBook, Unit


def create_image(
    name: str = "default.png", size: tuple[int, int] = (100, 100)
) -> SimpleUploadedFile:
    file: BytesIO = BytesIO()
    image: Image.Image = Image.new("RGB", size=size)
    image.save(file, "png")
    file.name = name
    file.seek(0)
    return SimpleUploadedFile(
        name=file.name, content=file.read(), content_type="image/png"
    )


class ChoiceTestCase(TestCase):
    def setUp(self) -> None:
        self.subject: Subject = Subject.objects.create(name="Mathematics")
        self.textbook: TextBook = TextBook.objects.create(
            subject=self.subject, title="Math Textbook"
        )
        self.unit: Unit = Unit.objects.create(text_book=self.textbook, title="Algebra")
        self.chapter: Chapter = Chapter.objects.create(
            unit=self.unit, title="Linear Equations"
        )
        self.lesson: Lesson = Lesson.objects.create(
            chapter=self.chapter, title="Solving Linear Equations"
        )
        self.question_type: Type = Type.objects.create(
            subject=self.subject, name="Multiple Choice"
        )
        self.question: Question = Question.objects.create(
            lesson=self.lesson,
            type=self.question_type,
            difficulty=Question.Difficulty.MEDIUM,
            body="What is the solution to the equation 2x + 3 = 7?",
        )
        self.choice: Choice = Choice.objects.create(
            question=self.question, body="x = 2", is_correct=True
        )

    def test_choice_creation(self) -> None:
        self.assertIsInstance(self.choice.id, UUID)
        self.assertEqual(self.choice.body, "x = 2")
        self.assertTrue(self.choice.is_correct)
        self.assertFalse(self.choice.figure)

    def test_choice_str_representation(self) -> None:
        self.assertEqual(str(self.choice), "x = 2")

    def test_choice_with_figure(self) -> None:
        another_question: Question = Question.objects.create(
            lesson=self.lesson,
            type=self.question_type,
            difficulty=Question.Difficulty.MEDIUM,
            body="a graph choices question",
        )
        image: SimpleUploadedFile = create_image()
        choice_with_figure: Choice = Choice.objects.create(
            question=another_question, figure=image, is_correct=False
        )
        self.assertIsNotNone(choice_with_figure.figure)
        self.assertTrue(
            choice_with_figure.figure.name.startswith(
                f"questions/{another_question.id}/choices/"
            )
        )

    def test_update_choice(self) -> None:
        self.choice.body = "x = 3"
        self.choice.is_correct = False
        self.choice.save()

        self.choice.refresh_from_db()

        self.assertEqual(self.choice.body, "x = 3")
        self.assertFalse(self.choice.is_correct)

    def test_cascade_delete_question(self) -> None:
        choice_id: UUID = self.choice.id
        self.question.delete()

        with self.assertRaises(Choice.DoesNotExist):
            Choice.objects.get(id=choice_id)

    def test_multiple_choices_for_question(self) -> None:
        Choice.objects.create(question=self.question, body="x = 1", is_correct=False)
        Choice.objects.create(question=self.question, body="x = 3", is_correct=False)

        choices: QuerySet = self.question.choices.all()
        self.assertEqual(choices.count(), 3)
        self.assertEqual(choices.filter(is_correct=True).count(), 1)

    def test_choice_ordering(self) -> None:
        Choice.objects.create(question=self.question, body="x = 1", is_correct=False)
        Choice.objects.create(question=self.question, body="x = 3", is_correct=False)

        choices: list[Choice] = list(Choice.objects.all())
        self.assertEqual(len(choices), 3)
        self.assertTrue(
            choices[0].created_at >= choices[1].created_at >= choices[2].created_at
        )

    def test_choice_with_only_figure(self) -> None:
        another_question: Question = Question.objects.create(
            lesson=self.lesson,
            type=self.question_type,
            difficulty=Question.Difficulty.MEDIUM,
            body="a graph choices question",
        )
        image: SimpleUploadedFile = create_image()
        choice_with_only_figure: Choice = Choice.objects.create(
            question=another_question, figure=image, is_correct=False
        )
        self.assertIsNotNone(choice_with_only_figure.figure)
        self.assertIsNone(choice_with_only_figure.body)
        self.assertEqual(
            str(choice_with_only_figure), choice_with_only_figure.figure.name
        )

    def test_choice_figure_path(self) -> None:
        another_question: Question = Question.objects.create(
            lesson=self.lesson,
            type=self.question_type,
            difficulty=Question.Difficulty.MEDIUM,
            body="a graph choices question",
        )
        image = create_image()
        choice_with_figure = Choice.objects.create(
            question=another_question, figure=image, is_correct=False
        )
        expected_path = (
            f"questions/{another_question.id}/choices/{choice_with_figure.id}"
        )
        self.assertTrue(choice_with_figure.figure.name.startswith(expected_path))

    def test_create_four_choices(self) -> None:
        another_question: Question = Question.objects.create(
            lesson=self.lesson,
            type=self.question_type,
            difficulty=Question.Difficulty.MEDIUM,
            body="a text choices question",
        )
        Choice.objects.create(question=another_question, body="x = 1", is_correct=False)
        Choice.objects.create(question=another_question, body="x = 2", is_correct=True)
        Choice.objects.create(question=another_question, body="x = 3", is_correct=False)
        Choice.objects.create(question=another_question, body="x = 4", is_correct=False)

        self.assertEqual(another_question.choices.count(), 4)
        self.assertEqual(another_question.choices.filter(is_correct=True).count(), 1)

    def test_cannot_create_more_than_four_choices(self) -> None:
        another_question: Question = Question.objects.create(
            lesson=self.lesson,
            type=self.question_type,
            difficulty=Question.Difficulty.MEDIUM,
            body="a text choices question",
        )
        Choice.objects.create(question=another_question, body="x = 1", is_correct=False)
        Choice.objects.create(question=another_question, body="x = 2", is_correct=True)
        Choice.objects.create(question=another_question, body="x = 3", is_correct=False)
        Choice.objects.create(question=another_question, body="x = 4", is_correct=False)
        with self.assertRaises(ValidationError):
            Choice.objects.create(
                question=another_question, body="x = 5", is_correct=False
            )

    def test_update_one_of_four_choices(self) -> None:
        another_question: Question = Question.objects.create(
            lesson=self.lesson,
            type=self.question_type,
            difficulty=Question.Difficulty.MEDIUM,
            body="a text choices question",
        )
        Choice.objects.create(question=another_question, body="x = 1", is_correct=False)
        Choice.objects.create(question=another_question, body="x = 2", is_correct=True)
        Choice.objects.create(question=another_question, body="x = 3", is_correct=False)
        to_update: Choice = Choice.objects.create(
            question=another_question, body="x = 4", is_correct=False
        )
        to_update.body = "x = 5"
        to_update.save()
        self.assertEqual(to_update.body, "x = 5")
        self.assertEqual(Choice.objects.get(pk=to_update.id).body, "x = 5")

    def test_cannot_have_multiple_correct_choices(self) -> None:
        Choice.objects.create(question=self.question, body="x = 1", is_correct=False)
        with self.assertRaises(ValidationError):
            Choice.objects.create(question=self.question, body="x = 2", is_correct=True)

        with self.assertRaises(ValidationError):
            Choice.objects.create(question=self.question, body="x = 3", is_correct=True)

    def test_choices_must_be_same_type(self) -> None:
        Choice.objects.create(question=self.question, body="x = 1", is_correct=False)

        with self.assertRaises(ValidationError):
            Choice.objects.create(
                question=self.question, figure=create_image(), is_correct=False
            )

    def test_choice_cannot_have_both_body_and_figure(self) -> None:
        with self.assertRaises(ValidationError):
            Choice.objects.create(
                question=self.question,
                body="x = 1",
                figure=create_image(),
                is_correct=False,
            )

    def test_four_figure_choices(self) -> None:
        another_question: Question = Question.objects.create(
            lesson=self.lesson,
            type=self.question_type,
            difficulty=Question.Difficulty.MEDIUM,
            body="a graph choices question",
        )
        Choice.objects.create(
            question=another_question, figure=create_image("1.png"), is_correct=False
        )
        Choice.objects.create(
            question=another_question, figure=create_image("2.png"), is_correct=True
        )
        Choice.objects.create(
            question=another_question, figure=create_image("3.png"), is_correct=False
        )
        Choice.objects.create(
            question=another_question, figure=create_image("4.png"), is_correct=False
        )

        self.assertEqual(another_question.choices.count(), 4)
        self.assertEqual(another_question.choices.filter(is_correct=True).count(), 1)
        self.assertTrue(all(choice.figure for choice in another_question.choices.all()))
