from datetime import datetime
from io import BytesIO
from uuid import UUID

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.query import QuerySet
from django.test import TestCase
from PIL import Image
from resources.models import Chapter, Subject, TextBook, Unit


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
        self.motion_1D: Chapter = Chapter.objects.create(
            unit=self.mechanics,
            title="motion in one dimension",
            caption="In this chapter,"
            + " we introduce the concept of motion in one dimension",
            cover=create_image(name="motion_in_1D.png", size=(100, 100)),
            syllabus_order=1,
        )
        self.kinematic: Chapter = Chapter.objects.create(
            unit=self.mechanics,
            title="Kinematic equations",
            caption="This chapter focuses on kinematic equations",
            cover=create_image(name="kinematic_equations.png", size=(200, 200)),
            syllabus_order=2,
        )
        self.newton: Chapter = Chapter.objects.create(
            unit=self.mechanics,
            title="Newton's laws",
            caption="This chapter focuses on Newton's laws of motion",
            cover=create_image(name="newton.png", size=(300, 300)),
            syllabus_order=3,
        )
        self.coloumb: Chapter = Chapter.objects.create(
            unit=self.electricity,
            title="Coloumb's law",
            caption="This chapter focuses on Coloumb's law",
            cover=create_image(name="coloumb.png", size=(400, 400)),
            syllabus_order=1,
        )
        self.gauss: Chapter = Chapter.objects.create(
            unit=self.electricity,
            title="Gauss's law",
            caption="This chapter focuses on Gauss's law",
            cover=create_image(name="gauss.png", size=(500, 500)),
            syllabus_order=2,
        )

    def test_str(self) -> None:
        self.assertEqual(str(self.motion_1D), "motion in one dimension")
        self.assertEqual(str(self.kinematic), "Kinematic equations")
        self.assertEqual(str(self.newton), "Newton's laws")
        self.assertEqual(str(self.coloumb), "Coloumb's law")
        self.assertEqual(str(self.gauss), "Gauss's law")

    def test_ordering(self) -> None:
        self.assertEqual(
            list(Chapter.objects.filter(unit=self.mechanics)),
            [self.motion_1D, self.kinematic, self.newton],
        )

    def test_chapter_title_is_required(self) -> None:
        with self.assertRaises(ValidationError):
            Chapter.objects.create(
                unit=self.algebra,
                title="",
                caption="This is a chapter",
                cover=create_image(),
            )
        with self.assertRaises(ValidationError):
            Chapter.objects.create(
                unit=self.algebra,
                title=None,  # type: ignore
                caption="This is a chapter",
                cover=create_image(),
            )

    def test_chapter_caption_is_optional(self) -> None:
        no_caption_chapter: Chapter = Chapter.objects.create(
            unit=self.algebra,
            title="A chapter",
            caption="",
            cover=create_image(),
            syllabus_order=1,
        )
        self.assertIsInstance(no_caption_chapter, Chapter)
        no_caption_chapter = Chapter.objects.create(
            unit=self.algebra,
            title="A chapter",
            caption=None,
            cover=create_image(),
            syllabus_order=2,
        )
        self.assertIsInstance(no_caption_chapter, Chapter)

    def test_unit_cover_is_optional(self) -> None:
        no_cover_chapter: Chapter = Chapter.objects.create(
            unit=self.algebra,
            title="A chapter",
            caption="This is a chapter",
            cover=None,
            syllabus_order=2,
        )
        self.assertIsInstance(no_cover_chapter, Chapter)
        no_cover_chapter = Chapter.objects.create(
            unit=self.algebra,
            title="Another chapter",
            caption="This is another chapter",
            cover=None,
            syllabus_order=3,
        )
        self.assertIsInstance(no_cover_chapter, Chapter)

    def test_unit_has_id_and_it_is_uuid(self) -> None:
        self.assertIsNotNone(self.newton.id)
        self.assertIsInstance(self.gauss.id, UUID)

    def test_unit_has_created_at_and_it_is_datetime(self) -> None:
        self.assertIsNotNone(self.motion_1D.created_at)
        self.assertIsInstance(self.kinematic.created_at, datetime)

    def test_unit_has_updated_at_and_it_is_datetime(self) -> None:
        self.assertIsNotNone(self.coloumb.updated_at)
        self.assertIsInstance(self.newton.updated_at, datetime)
        last_update: datetime = self.coloumb.updated_at
        self.coloumb.title = "coloumb updated"
        self.coloumb.save()
        self.assertGreater(self.coloumb.updated_at, last_update)

    def test_image_name_after_saving(self) -> None:
        self.assertRegex(
            self.motion_1D.cover.name,
            r"covers\/Chapter\/motion-in-one-dimension._(.*).png",
        )
        self.assertRegex(
            self.newton.cover.name, r"covers\/Chapter\/newtons-laws._(.*).png"
        )
        self.assertRegex(
            self.gauss.cover.name, r"covers\/Chapter\/gausss-law._(.*).png"
        )

    def test_image_size_after_saving(self) -> None:
        """this test ensures that any image with size over (300, 300)
        will be resized to (300, 300)"""
        image: Image.Image = Image.open(self.motion_1D.cover)
        self.assertEqual(image.size, (100, 100))
        image = Image.open(self.kinematic.cover)
        self.assertEqual(image.size, (200, 200))
        image = Image.open(self.newton.cover)
        self.assertEqual(image.size, (300, 300))  # was (300, 300)
        image = Image.open(self.coloumb.cover)
        self.assertEqual(image.size, (300, 300))  # was (400, 400)
        image = Image.open(self.gauss.cover)
        self.assertEqual(image.size, (300, 300))  # was (500, 500)

    def test_max_length_of_title(self) -> None:
        with self.assertRaises(ValidationError):
            Chapter.objects.create(
                unit=self.algebra,
                title="A" * 256,
                caption="This is a chapter",
                cover=create_image(),
                syllabus_order=5,
            )

    def test_unit_is_required(self) -> None:
        with self.assertRaises(ValidationError):
            Chapter.objects.create(
                unit=None,  # type: ignore
                title="A chapter",
                caption="This is a chapter",
                cover=create_image(),
                syllabus_order=5,
            )

    def test_getting_chapters_of_a_unit(self) -> None:
        mechanics_chapters: QuerySet = Chapter.objects.filter(unit=self.mechanics)
        self.assertEqual(mechanics_chapters.count(), 3)
        self.assertEqual(mechanics_chapters[0].title, "motion in one dimension")
        self.assertEqual(mechanics_chapters[1].title, "Kinematic equations")
        self.assertEqual(mechanics_chapters[2].title, "Newton's laws")
        Chapter.objects.create(
            title="Another chapter of mechanics unit",
            caption="This is another chapter",
            unit=self.mechanics,
            cover=create_image(name="another_mechanics_chapter.png", size=(100, 100)),
            syllabus_order=5,
        )
        mechanics_chapters = Chapter.objects.filter(unit=self.mechanics)
        self.assertEqual(mechanics_chapters.count(), 4)
        self.assertEqual(
            mechanics_chapters[3].title, "Another chapter of mechanics unit"
        )

    def test_unit_has_a_syllabus_order(self) -> None:
        self.assertEqual(self.motion_1D.syllabus_order, 1)
        self.assertEqual(self.newton.syllabus_order, 3)
        self.assertEqual(self.coloumb.syllabus_order, 1)
        self.assertEqual(self.gauss.syllabus_order, 2)

    def test_chapter_with_updated_unit(self):
        self.assertEqual(self.motion_1D.unit, self.mechanics)
        self.motion_1D.syllabus_order = 5
        self.motion_1D.unit = self.algebra
        self.motion_1D.save()
        self.assertEqual(self.motion_1D.unit, self.algebra)
        self.assertEqual(Chapter.objects.filter(unit=self.algebra).count(), 1)
        self.assertEqual(Chapter.objects.filter(unit=self.mechanics).count(), 2)

    def test_unit_of_a_chapter(self):
        self.assertEqual(self.motion_1D.unit, self.mechanics)
        self.assertEqual(self.gauss.unit, self.electricity)
        self.mechanics.title = "newtonian mechanics"
        self.mechanics.save()
        self.motion_1D.refresh_from_db()
        self.assertEqual(self.motion_1D.unit, self.mechanics)
        self.assertEqual(self.motion_1D.unit.title, "newtonian mechanics")

    def text_all_chapters_from_unit(self):
        self.assertEqual(self.mechanics.chapters.count(), 3)
        self.assertEqual(self.electricity.chapters.count(), 2)
        self.assertEqual(
            self.mechanics.chapters.first().title,  # type: ignore
            "motion in one dimension",
        )
        self.assertEqual(
            self.mechanics.chapters.last().title, "Newton's laws"  # type: ignore
        )
        self.assertEqual(
            self.electricity.chapters.first().title, "Coloumb's law"  # type: ignore
        )
        self.assertEqual(
            self.electricity.chapters.last().title, "Gauss's law"  # type: ignore
        )
