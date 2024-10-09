from datetime import datetime
from io import BytesIO
from uuid import UUID

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.query import QuerySet
from django.test import TestCase
from PIL import Image
from resources.models import Subject, TextBook, Unit


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


class TestUnit(TestCase):
    def setUp(self) -> None:
        self.math: Subject = Subject.objects.create(name="Math")
        self.physics: Subject = Subject.objects.create(name="Physics")
        self.math_book1: TextBook = TextBook.objects.create(
            subject=self.math,
            title="Math Book 1",
            caption="This textbook is number 1 for math subject",
            cover=create_image(name="mathBook1.png", size=(100, 100)),
        )
        self.physics_book1: TextBook = TextBook.objects.create(
            subject=self.physics,
            title="Physics Book 1",
            caption="This textbook is number 1 for physics subject",
            cover=create_image(name="physicsBook1.png", size=(200, 200)),
        )
        self.math_book2: TextBook = TextBook.objects.create(
            subject=self.math,
            title="Math Book 2",
            caption="This textbook is number 2 for math subject",
            cover=create_image(name="mathBook2.png", size=(300, 300)),
        )
        self.physics_book2: TextBook = TextBook.objects.create(
            subject=self.physics,
            title="Biology Book 2",
            caption="This textbook is number 2 for physics subject",
            cover=create_image(name="physicsBook.png", size=(301, 301)),
        )
        self.mechanics: Unit = Unit.objects.create(
            text_book=self.physics_book1,
            title="Mechanics",
            caption="This unit is about classical mechanics",
            cover=create_image(name="mechanics.png", size=(100, 400)),
            syllabus_order=1,
        )
        self.electricity: Unit = Unit.objects.create(
            text_book=self.physics_book1,
            title="Electricity",
            caption="This unit is about electricity",
            cover=create_image(name="electricity.png", size=(200, 300)),
            syllabus_order=2,
        )
        self.waves: Unit = Unit.objects.create(
            text_book=self.physics_book2,
            title="Waves",
            caption="This unit is about waves",
            cover=create_image(name="waves.png", size=(300, 200)),
            syllabus_order=1,
        )
        self.optics: Unit = Unit.objects.create(
            text_book=self.physics_book2,
            title="Optics",
            caption="This unit is about optics",
            cover=create_image(name="optics.png", size=(400, 100)),
            syllabus_order=2,
        )
        self.algebra: Unit = Unit.objects.create(
            text_book=self.math_book1,
            title="Algebra",
            caption="This unit is about algebra",
            cover=create_image(name="algebra.png", size=(100, 100)),
            syllabus_order=1,
        )
        self.geometry: Unit = Unit.objects.create(
            text_book=self.math_book1,
            title="Geometry",
            caption="This unit is about geometry",
            cover=create_image(name="geometry.png", size=(200, 200)),
            syllabus_order=2,
        )
        self.calculus: Unit = Unit.objects.create(
            text_book=self.math_book2,
            title="Calculus",
            caption="This unit is about calculus",
            cover=create_image(name="calculus.png", size=(300, 300)),
            syllabus_order=1,
        )
        self.trigonometry: Unit = Unit.objects.create(
            text_book=self.math_book2,
            title="Trigonometry",
            caption="This unit is about trigonometry",
            cover=create_image(name="trigonometry.png", size=(400, 400)),
            syllabus_order=2,
        )

    def test_str(self) -> None:
        self.assertEqual(str(self.mechanics), "Mechanics")
        self.assertEqual(str(self.electricity), "Electricity")
        self.assertEqual(str(self.waves), "Waves")
        self.assertEqual(str(self.optics), "Optics")
        self.assertEqual(str(self.algebra), "Algebra")
        self.assertEqual(str(self.geometry), "Geometry")
        self.assertEqual(str(self.calculus), "Calculus")
        self.assertEqual(str(self.trigonometry), "Trigonometry")

    def test_ordering(self) -> None:
        Unit.objects.create(
            text_book=self.math_book1,
            title="Another unit of Math Book 1",
            caption="This is another unit of math book number 1",
            cover=create_image(name="another_math_unit.png", size=(100, 100)),
            syllabus_order=4,
        )
        Unit.objects.create(
            text_book=self.math_book1,
            title="Another unit of Math Book 1",
            caption="This is another unit of math book number 1",
            cover=create_image(name="another_math_unit.png", size=(100, 100)),
            syllabus_order=5,
        )
        Unit.objects.create(
            text_book=self.math_book1,
            title="Another unit of Math Book 1",
            caption="This is another unit of math book number 1",
            cover=create_image(name="another_math_unit.png", size=(100, 100)),
            syllabus_order=3,
        )
        self.assertEqual(
            list(
                Unit.objects.filter(text_book=self.math_book1).values_list(
                    "title", flat=True
                )
            ),
            [
                "Algebra",
                "Geometry",
                "Another unit of Math Book 1",
                "Another unit of Math Book 1",
                "Another unit of Math Book 1",
            ],
        )

    def test_unit_title_is_required(self) -> None:
        with self.assertRaises(ValidationError):
            Unit.objects.create(
                text_book=self.math_book1,
                title="",
                caption="This is a unit",
                cover=create_image(),
            )

    def test_unit_caption_is_optional(self) -> None:
        no_caption_unit: Unit = Unit.objects.create(
            text_book=self.math_book1,
            title="A Unit",
            caption="",
            cover=create_image(),
            syllabus_order=9,
        )
        self.assertIsInstance(no_caption_unit, Unit)
        no_caption_unit = Unit.objects.create(
            text_book=self.math_book1,
            title="Another Unit",
            caption=None,
            cover=create_image(),
            syllabus_order=10,
        )
        self.assertIsInstance(no_caption_unit, Unit)

    def test_unit_cover_is_optional(self) -> None:
        no_cover_unit: Unit = Unit.objects.create(
            text_book=self.math_book1,
            title="A Unit",
            caption="This is a unit",
            cover="",
            syllabus_order=9,
        )
        self.assertIsInstance(no_cover_unit, Unit)
        no_cover_unit = Unit.objects.create(
            text_book=self.math_book1,
            title="A Unit",
            caption="This is a unit",
            cover=None,
            syllabus_order=10,
        )
        self.assertIsInstance(no_cover_unit, Unit)

    def test_unit_has_id_and_it_is_uuid(self) -> None:
        self.assertIsNotNone(self.mechanics.id)
        self.assertIsInstance(self.electricity.id, UUID)

    def test_unit_has_created_at_and_it_is_datetime(self) -> None:
        self.assertIsNotNone(self.mechanics.created_at)
        self.assertIsInstance(self.electricity.created_at, datetime)

    def test_unit_has_updated_at_and_it_is_datetime(self) -> None:
        self.assertIsNotNone(self.mechanics.updated_at)
        self.assertIsInstance(self.electricity.updated_at, datetime)

    def test_image_name_after_saving(self) -> None:
        self.assertRegex(self.algebra.cover.name, r"covers\/Unit\/algebra._(.*).png")
        self.assertRegex(
            self.mechanics.cover.name, r"covers\/Unit\/mechanics._(.*).png"
        )
        self.assertRegex(
            self.trigonometry.cover.name, r"covers\/Unit\/trigonometry._(.*).png"
        )

    def test_image_size_after_saving(self) -> None:
        """this test ensures that any image with size over (300, 300)
        will be resized to (300, 300)"""
        image: Image.Image = Image.open(self.algebra.cover)
        self.assertEqual(image.size, (100, 100))
        image = Image.open(self.mechanics.cover)
        self.assertEqual(image.size, (75, 300))
        image = Image.open(self.trigonometry.cover)
        self.assertEqual(image.size, (300, 300))
        image = Image.open(self.optics.cover)
        self.assertEqual(image.size, (300, 75))
        image = Image.open(self.waves.cover)
        self.assertEqual(image.size, (300, 200))
        image = Image.open(self.electricity.cover)
        self.assertEqual(image.size, (200, 300))
        image = Image.open(self.geometry.cover)
        self.assertEqual(image.size, (200, 200))
        image = Image.open(self.calculus.cover)
        self.assertEqual(image.size, (300, 300))

    def test_max_length_of_title(self) -> None:
        with self.assertRaises(ValidationError):
            Unit.objects.create(
                text_book=self.math_book1,
                title="A" * 256,
                caption="This is a unit",
                cover=create_image(),
                syllabus_order=10,
            )

    def test_text_book_is_required(self) -> None:
        with self.assertRaises(ValidationError):
            Unit.objects.create(
                text_book=None,  # type: ignore
                title="A Unit",
                caption="This is a unit",
                cover=create_image(),
                syllabus_order=10,
            )

    def test_getting_units_of_a_textbook(self) -> None:
        math_book1_units: QuerySet = Unit.objects.filter(text_book=self.math_book1)
        self.assertEqual(math_book1_units.count(), 2)
        self.assertEqual(math_book1_units[0].title, "Algebra")
        self.assertEqual(math_book1_units[1].title, "Geometry")
        Unit.objects.create(
            title="Another unit of Math Book 1",
            caption="This is another unit of math book number 1",
            text_book=self.math_book1,
            cover=create_image(name="another_math_unit.png", size=(100, 100)),
            syllabus_order=3,
        )
        math_book1_units = Unit.objects.filter(text_book=self.math_book1)
        self.assertEqual(math_book1_units.count(), 3)
        # the first book should be the Another Math Book
        # because it is syllaus_order = 1
        self.assertEqual(math_book1_units[0].title, "Algebra")

    def test_unit_has_a_syllabus_order(self) -> None:
        self.assertEqual(self.algebra.syllabus_order, 1)
        self.assertEqual(self.geometry.syllabus_order, 2)
        self.assertEqual(self.calculus.syllabus_order, 1)
        self.assertEqual(self.trigonometry.syllabus_order, 2)

    def test_unit_with_updated_textbook(self) -> None:
        self.assertEqual(self.mechanics.text_book, self.physics_book1)
        self.mechanics.syllabus_order = 3
        self.mechanics.text_book = self.physics_book2
        self.mechanics.save()
        self.assertEqual(self.mechanics.text_book, self.physics_book2)
        self.assertEqual(Unit.objects.filter(text_book=self.physics_book2).count(), 3)
        self.assertEqual(Unit.objects.filter(text_book=self.physics_book1).count(), 1)
        self.assertEqual(Unit.objects.filter(text_book=self.math_book2).count(), 2)

    def test_textbook_of_a_unit(self) -> None:
        self.assertEqual(self.algebra.text_book, self.math_book1)
        self.assertEqual(self.electricity.text_book, self.physics_book1)
        self.physics_book1.title = "classical physics"
        self.physics_book1.save()
        self.electricity.refresh_from_db()
        self.assertEqual(self.electricity.text_book, self.physics_book1)
        self.assertEqual(self.electricity.text_book.title, "classical physics")

    def text_all_units_from_textbook(self) -> None:
        self.assertEqual(self.math_book1.units.count(), 2)
        self.assertEqual(self.math_book2.units.count(), 2)
        self.assertEqual(self.physics_book1.units.count(), 2)
        self.assertEqual(self.physics_book2.units.count(), 2)
        self.assertEqual(self.math_book1.units.first().title, "Algebra")
        self.assertEqual(self.math_book1.units.last().title, "Geometry")
        self.assertEqual(self.math_book2.units.first().title, "Calculus")
        self.assertEqual(self.math_book2.units.last().title, "Trigonometry")
        self.assertEqual(self.physics_book1.units.first().title, "Mechanics")
        self.assertEqual(self.physics_book1.units.last().title, "Electricity")
        self.assertEqual(self.physics_book2.units.first().title, "Waves")
        self.assertEqual(self.physics_book2.units.last().title, "Optics")
