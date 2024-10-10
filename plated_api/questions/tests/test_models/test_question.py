from datetime import datetime
from io import BytesIO
from uuid import UUID

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import QuerySet
from django.test import TestCase
from PIL import Image
from questions.models import Question, Type
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


class QuestionTestCase(TestCase):
    def setUp(self) -> None:
        self.q_physics: Subject = Subject.objects.create(name="q_Physics")
        self.textbook: TextBook = TextBook.objects.create(
            subject=self.q_physics, title="Physics Textbook"
        )
        self.unit: Unit = Unit.objects.create(text_book=self.textbook, title="Unit 1")
        self.chapter: Chapter = Chapter.objects.create(
            unit=self.unit, title="Chapter 1"
        )
        self.lesson: Lesson = Lesson.objects.create(
            chapter=self.chapter, title="Lesson 1"
        )

        self.single_step_question: Type = Type.objects.create(
            subject=self.q_physics,
            name="Single-Step question",
            description="A question that can be answered in one step.",
        )
        self.computational_question: Type = Type.objects.create(
            subject=self.q_physics,
            name="Computational question",
            description="Involves performing calculations to find the answer.",
        )
        self.qualitative_question: Type = Type.objects.create(
            subject=self.q_physics,
            name="Qualitative question",
            description=(
                "Involves reasoning and explanation "
                "rather than numerical calculations."
            ),
        )
        self.graphical_question: Type = Type.objects.create(
            subject=self.q_physics,
            name="Graphical question",
            description="Involves interpreting or drawing graphs to find the solution.",
        )

        self.q1: Question = Question.objects.create(
            type=self.single_step_question,
            difficulty=Question.Difficulty.EASY,
            body=(
                "A car travels 100 km at a speed of 50 km/h. "
                "How long does the journey take?"
            ),
            lesson=self.lesson,
        )

        self.q2: Question = Question.objects.create(
            type=self.computational_question,
            difficulty=Question.Difficulty.MEDIUM,
            body=(
                "What is the kinetic energy of a 3 kg object moving at 4 m/s? "
                "Use the formula KE = 1/2 mv^2."
            ),
            lesson=self.lesson,
        )

        self.q3: Question = Question.objects.create(
            type=self.qualitative_question,
            difficulty=Question.Difficulty.EASY,
            body=(
                "Why do objects in free fall (in a vacuum) fall at the same rate, "
                "regardless of their mass? "
                "Explain the concept of gravitational acceleration."
            ),
            lesson=self.lesson,
        )

        self.q4: Question = Question.objects.create(
            type=self.graphical_question,
            difficulty=Question.Difficulty.MEDIUM,
            body=(
                "The opposite graph represents the change in velocity of a moving car"
                "with time. Calculate the slope of the graph."
            ),
            lesson=self.lesson,
            figure=create_image(name="v-t graph.png", size=(200, 200)),
        )

    def test_question_creation(self) -> None:
        """Test if questions are created correctly"""
        # Test Single-Step Question
        self.assertEqual(self.q1.type.name, "Single-Step question")  # type: ignore
        self.assertEqual(self.q1.difficulty, Question.Difficulty.EASY)
        self.assertEqual(self.q1.lesson, self.lesson)

        # since self.q1.figure returns <ImageFieldFile: None> and not None
        # ImageFieldFile subclasses File, which defines:
        # def __nonzero__(self):
        #     return bool(self.name)
        # Thus, we check for a boolean where True means ther is an image
        self.assertFalse(self.q1.figure)

        # Test Computational Question
        self.assertEqual(self.q2.type.name, "Computational question")  # type: ignore
        self.assertEqual(self.q2.difficulty, Question.Difficulty.MEDIUM)
        self.assertFalse(self.q2.figure)

        # Test Qualitative Question
        self.assertEqual(self.q3.type.name, "Qualitative question")  # type: ignore
        self.assertEqual(self.q3.difficulty, Question.Difficulty.EASY)
        self.assertFalse(self.q3.figure)

        # Test Graphical Question
        self.assertEqual(self.q4.type.name, "Graphical question")  # type: ignore
        self.assertEqual(self.q4.difficulty, Question.Difficulty.MEDIUM)
        self.assertTrue(self.q4.figure)
        self.assertTrue(self.q4.figure.name.endswith("v-t_graph.png"))

    def test_question_has_id_is_uuid(self) -> None:
        """Test if questions have a unique id"""
        self.assertTrue(self.q1.id)
        self.assertTrue(self.q2.id)
        self.assertTrue(self.q3.id)
        self.assertTrue(self.q4.id)
        self.assertIsInstance(self.q1.id, UUID)
        self.assertIsInstance(self.q2.id, UUID)
        self.assertIsInstance(self.q3.id, UUID)
        self.assertIsInstance(self.q4.id, UUID)

    def test_question_has_created_at_is_datetime(self) -> None:
        """Test if questions have a created_at field"""
        self.assertTrue(self.q1.created_at)
        self.assertTrue(self.q2.created_at)
        self.assertTrue(self.q3.created_at)
        self.assertTrue(self.q4.created_at)
        self.assertIsInstance(self.q1.created_at, datetime)
        self.assertIsInstance(self.q2.created_at, datetime)
        self.assertIsInstance(self.q3.created_at, datetime)
        self.assertIsInstance(self.q4.created_at, datetime)

    def test_question_has_updated_at_is_datetime(self) -> None:
        """Test if questions have an updated_at field"""
        self.assertTrue(self.q1.updated_at)
        self.assertTrue(self.q2.updated_at)
        self.assertTrue(self.q3.updated_at)
        self.assertTrue(self.q4.updated_at)
        self.assertIsInstance(self.q1.updated_at, datetime)
        self.assertIsInstance(self.q2.updated_at, datetime)
        self.assertIsInstance(self.q3.updated_at, datetime)
        self.assertIsInstance(self.q4.updated_at, datetime)

    def test_update_at_is_updated(self) -> None:
        old_updated_at: datetime = self.q1.updated_at
        self.q1.body = (
            "A car travels 100 km at a speed of 50 km/h. How long does it take?"
        )
        self.q1.save()
        self.assertNotEqual(old_updated_at, self.q1.updated_at)

    def test_question_str(self) -> None:
        """Test if questions are represented as strings"""
        self.assertEqual(
            str(self.q1), "A car travels 100 km at a speed of 50 km/h. How lo"
        )
        self.assertEqual(len(str(self.q1)), 50)
        self.assertEqual(
            str(self.q2), "What is the kinetic energy of a 3 kg object moving"
        )
        self.assertEqual(len(str(self.q2)), 50)
        self.assertEqual(
            str(self.q3),
            "Why do objects in free fall (in a vacuum) fall at ",
        )
        self.assertEqual(len(str(self.q3)), 50)
        self.assertEqual(
            str(self.q4), "The opposite graph represents the change in veloci"
        )
        self.assertEqual(len(str(self.q4)), 50)

    def test_all_questions_of_a_lesson(self) -> None:
        questions: QuerySet = Question.objects.filter(lesson=self.lesson)
        self.assertEqual(questions.count(), 4)
        self.assertIn(self.q1, questions)
        self.assertIn(self.q2, questions)
        self.assertIn(self.q3, questions)
        self.assertIn(self.q4, questions)

        questions = self.lesson.questions.all()
        self.assertEqual(questions.count(), 4)
        self.assertIn(self.q1, questions)
        self.assertIn(self.q2, questions)
        self.assertIn(self.q3, questions)
        self.assertIn(self.q4, questions)

    def test_easy_questions(self) -> None:
        easy_questions: QuerySet = Question.objects.filter(
            difficulty=Question.Difficulty.EASY
        )
        self.assertEqual(easy_questions.count(), 2)
        self.assertIn(self.q1, easy_questions)
        self.assertIn(self.q3, easy_questions)

    def test_graph_questions(self) -> None:
        graph_questions: QuerySet = Question.objects.filter(
            type=self.graphical_question
        )
        self.assertEqual(graph_questions.count(), 1)
        self.assertIn(self.q4, graph_questions)

    def test_default_difficulty(self) -> None:
        q5: Question = Question.objects.create(
            type=self.single_step_question, body="Test question", lesson=self.lesson
        )
        self.assertEqual(q5.difficulty, Question.Difficulty.EASY)

    def test_difficulty_choice_out_of_choices(self) -> None:
        with self.assertRaises(ValidationError):
            Question.objects.create(
                type=self.single_step_question,
                body="Test question",
                lesson=self.lesson,
                difficulty="very easy",
            )

    def test_update_question(self):
        # Test updating a question
        self.q1.body = "What is the speed of sound?"
        self.q1.difficulty = Question.Difficulty.MEDIUM
        self.q1.save()

        # Refresh from database
        self.q1.refresh_from_db()

        self.assertEqual(self.q1.body, "What is the speed of sound?")
        self.assertEqual(self.q1.difficulty, Question.Difficulty.MEDIUM)

    def test_cascade_delete_lesson(self):
        # Test that deleting a lesson cascades to its questions
        lesson_id = self.lesson.id
        self.lesson.delete()

        # Check that the question no longer exists
        with self.assertRaises(Question.DoesNotExist):
            Question.objects.get(id=self.q1.id)

        # Check that the lesson no longer exists
        with self.assertRaises(Lesson.DoesNotExist):
            Lesson.objects.get(id=lesson_id)
