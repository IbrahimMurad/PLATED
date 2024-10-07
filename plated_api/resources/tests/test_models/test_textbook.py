from datetime import datetime
from io import BytesIO
from uuid import UUID

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.query import QuerySet
from django.test import TestCase
from PIL import Image
from resources.models import Subject, TextBook


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


class TestTextBook(TestCase):
    def setUp(self) -> None:
        self.math: Subject = Subject.objects.create(name="Math")
        self.physics: Subject = Subject.objects.create(name="Physics")
        self.english: Subject = Subject.objects.create(name="English")
        self.biology: Subject = Subject.objects.create(name="Biology")
        self.chemistry: Subject = Subject.objects.create(name="Chemistry")
        self.history: Subject = Subject.objects.create(name="History")
        self.geography: Subject = Subject.objects.create(name="Geography")
        self.computer_science: Subject = Subject.objects.create(name="Computer Science")
        self.economics: Subject = Subject.objects.create(name="Economics")
        self.math_book: TextBook = TextBook.objects.create(
            subject=self.math,
            title="Math Book",
            caption="This textbook is for math subject",
            cover=create_image(name="mathBook.png", size=(100, 100)),
        )
        self.physics_book: TextBook = TextBook.objects.create(
            subject=self.physics,
            title="Physics Book",
            caption="This textbook is for physics subject",
            cover=create_image(name="physicsBook.png", size=(200, 200)),
        )
        self.english_book: TextBook = TextBook.objects.create(
            subject=self.english,
            title="English Book",
            caption="This textbook is for english subject",
            cover=create_image(name="englishBook.png", size=(300, 300)),
        )
        self.biology_book: TextBook = TextBook.objects.create(
            subject=self.biology,
            title="Biology Book",
            caption="This textbook is for biology subject",
            cover=create_image(name="biologyBook.png", size=(301, 301)),
        )
        self.chemistry_book: TextBook = TextBook.objects.create(
            subject=self.chemistry,
            title="Chemistry Book",
            caption="This textbook is for chemistry subject",
            cover=create_image(name="chemistryBook.png", size=(400, 400)),
        )
        self.history_book: TextBook = TextBook.objects.create(
            subject=self.history,
            title="History Book",
            caption="This textbook is for history subject",
            cover=create_image(name="historyBook.png", size=(500, 500)),
        )
        self.geography_book: TextBook = TextBook.objects.create(
            subject=self.geography,
            title="Geography Book",
            caption="This textbook is for geography subject",
            cover=create_image(name="geographyBook.png", size=(50, 50)),
        )
        self.computer_science_book: TextBook = TextBook.objects.create(
            subject=self.computer_science,
            title="Computer Science Book",
            caption="This textbook is for computer science subject",
            cover=create_image(name="computer_sience_book.png", size=(299, 299)),
        )
        self.economics_book: TextBook = TextBook.objects.create(
            subject=self.economics,
            title="Economics Book",
            caption="This textbook is for economics subject",
            cover=create_image(name="economicsBook.png", size=(300, 300)),
        )

    def test_str(self) -> None:
        self.assertEqual(str(self.math_book), "Math Book")
        self.assertEqual(str(self.physics_book), "Physics Book")

    def test_ordering(self) -> None:
        all_testbooks: QuerySet = TextBook.objects.all()
        self.assertEqual(all_testbooks[0], self.biology_book)
        self.assertEqual(all_testbooks[1], self.chemistry_book)
        self.assertEqual(all_testbooks[2], self.computer_science_book)
        self.assertEqual(all_testbooks[3], self.economics_book)
        self.assertEqual(all_testbooks[4], self.english_book)
        self.assertEqual(all_testbooks[5], self.geography_book)
        self.assertEqual(all_testbooks[6], self.history_book)
        self.assertEqual(all_testbooks[7], self.math_book)
        self.assertEqual(all_testbooks[8], self.physics_book)

    def test_textbook_title_is_required(self) -> None:
        with self.assertRaises(ValidationError):
            TextBook.objects.create(
                title=None,  # type: ignore
                caption="a caption",
                subject=self.math,
                cover=create_image(),
            )

    def test_textbook_caption_is_optional(self) -> None:
        TextBook.objects.create(
            title="A Textbook",
            caption=None,
            subject=self.math,
            cover=create_image(),
        )

    def test_textbook_cover_is_optional(self) -> None:
        TextBook.objects.create(
            title="A Textbook",
            caption="A caption",
            subject=self.math,
            cover=None,
        )

    def test_textbook_has_id_and_it_is_uuid(self) -> None:
        self.assertIsNotNone(self.math_book.id)
        self.assertIsInstance(self.math_book.id, UUID)

    def test_textbook_has_created_at_and_it_is_datetime(self) -> None:
        self.assertIsNotNone(self.math.created_at)
        self.assertIsInstance(self.math.created_at, datetime)

    def test_textbook_has_updated_at_and_it_is_datetime(self) -> None:
        self.assertIsNotNone(self.math_book.updated_at)
        self.assertIsInstance(self.math_book.updated_at, datetime)

    def test_image_name_after_saving(self) -> None:
        self.assertRegex(
            self.math_book.cover.name, r"covers\/TextBook\/math-book._(.*).png"
        )
        self.assertRegex(
            self.physics_book.cover.name, r"covers\/TextBook\/physics-book._(.*).png"
        )
        self.assertRegex(
            self.english_book.cover.name, r"covers\/TextBook\/english-book._(.*).png"
        )

    def test_image_size_after_saving(self) -> None:
        """this test ensures that any image with size over (300, 300)
        will be resized to (300, 300)"""
        image: Image.Image = Image.open(self.math_book.cover)
        self.assertEqual(image.size, (100, 100))
        image = Image.open(self.physics_book.cover)
        self.assertEqual(image.size, (200, 200))
        image = Image.open(self.english_book.cover)
        self.assertEqual(image.size, (300, 300))  # was (300, 300)
        image = Image.open(self.biology_book.cover)
        self.assertEqual(image.size, (300, 300))  # was (301, 301)
        image = Image.open(self.chemistry_book.cover)
        self.assertEqual(image.size, (300, 300))  # was (400, 400)
        image = Image.open(self.history_book.cover)
        self.assertEqual(image.size, (300, 300))  # was (500, 500)
        image = Image.open(self.geography_book.cover)
        self.assertEqual(image.size, (50, 50))
        image = Image.open(self.computer_science_book.cover)
        self.assertEqual(image.size, (299, 299))
        image = Image.open(self.economics_book.cover)
        self.assertEqual(image.size, (300, 300))  # was (300, 300)

    def test_max_length_of_title(self) -> None:
        with self.assertRaises(ValidationError):
            TextBook.objects.create(
                title="A" * 256,
                caption="a caption",
                subject=self.math,
                cover=create_image(),
            )

    def test_subject_is_required(self) -> None:
        with self.assertRaises(ValidationError):
            TextBook.objects.create(
                title="A Textbook",
                caption="a caption",
                subject=None,  # type: ignore
                cover=create_image(),
            )

    def test_getting_textbooks_of_a_subject(self) -> None:
        math_books: QuerySet = TextBook.objects.filter(subject=self.math)
        self.assertEqual(math_books.count(), 1)
        self.assertEqual(math_books[0], self.math_book)
        TextBook.objects.create(
            title="Another Math Book",
            caption="This is another math book",
            subject=self.math,
            cover=create_image(name="anotherMathBook.png", size=(100, 100)),
        )
        math_books = TextBook.objects.filter(subject=self.math)
        self.assertEqual(math_books.count(), 2)
        # the first book should be the Another Math Book
        # because it is alphabetically first (ordered by title)
        self.assertEqual(math_books[0].title, "Another Math Book")

    def test_textbook_has_a_syllabus_order(self) -> None:
        self.assertIsNone(self.math_book.syllabus_order)
        self.assertIsNone(self.physics_book.syllabus_order)
        self.assertIsNone(self.english_book.syllabus_order)

    def test_textbook_with_updated_subject(self):
        self.assertEqual(self.math_book.subject, self.math)
        self.math_book.subject = self.physics
        self.math_book.save()
        self.assertEqual(self.math_book.subject, self.physics)
        self.assertEqual(TextBook.objects.filter(subject=self.math).count(), 0)
        self.assertEqual(TextBook.objects.filter(subject=self.physics).count(), 2)
        self.assertEqual(TextBook.objects.filter(subject=self.english).count(), 1)

    def test_subject_of_a_textbook(self):
        self.assertEqual(self.math_book.subject, self.math)
        self.assertEqual(self.physics_book.subject, self.physics)
        self.math.name = "Mathematics"
        self.math.save()
        self.math_book.refresh_from_db()
        self.assertEqual(self.math_book.subject, self.math)
        self.assertEqual(self.physics_book.subject, self.physics)
        self.assertEqual(self.math_book.subject.name, "Mathematics")
        self.assertEqual(self.physics_book.subject.name, "Physics")

    def text_all_textbooks_from_subject(self):
        self.assertEqual(self.math.textbooks.count(), 1)
        self.assertEqual(self.physics.textbooks.count(), 1)
        self.assertEqual(self.english.textbooks.first(), self.english_book)
        self.assertEqual(self.biology.textbooks.first(), self.biology_book)
        TextBook.objects.create(
            title="Another Math Book",
            caption="This is another math book",
            subject=self.math,
            cover=create_image(name="anotherMathBook.png", size=(100, 100)),
        )
        self.assertEqual(self.math.textbooks.count(), 2)
        self.assertEqual(self.physics.textbooks.count(), 1)
