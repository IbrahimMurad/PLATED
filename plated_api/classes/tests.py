from classes.models import Class
from core.models import BaseModel
from django.core.exceptions import ValidationError
from django.test import TestCase
from grades.models import Curriculum, Grade, Path, Stage
from resources.models import Subject
from users.models import Student, Teacher, User


class ClassModelTest(TestCase):
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
        self.grade: Grade = Grade.objects.create(
            name="First Grade", stage=self.stage, order_in_stage=1
        )
        self.subject: Subject = Subject.objects.create(name="Math")
        self.user_teacher = User.objects.create_user(
            email="teacher@tmail.com",
            username="teacher",
            password="teacherPass",
            role=User.Role.TEACHER,
        )
        self.user_student: User = User.objects.create_user(
            email="student@tmail.com",
            username="student",
            password="studentPass",
            role=User.Role.STUDENT,
        )
        self.teacher: Teacher = Teacher.objects.create(
            user=self.user_teacher, subject=self.subject, max_students=10
        )
        self.student: Student = Student.objects.create(
            user=self.user_student, grade=self.grade
        )

    def test_create_class(self) -> None:
        class_obj: Class = Class.objects.create(
            teacher=self.teacher, name="Math Class", grade=self.grade
        )
        self.assertEqual(class_obj.name, "Math Class")
        self.assertEqual(class_obj.teacher, self.teacher)
        self.assertEqual(class_obj.grade, self.grade)

    def test_Class_is_subclass_of_BaseModel(self) -> None:
        self.assertTrue(issubclass(Class, BaseModel))

    def test_class_string_representation(self) -> None:
        class_obj: Class = Class.objects.create(
            teacher=self.teacher, name="Science Class"
        )
        self.assertEqual(str(class_obj), "Science Class")

    def test_class_without_teacher(self) -> None:
        with self.assertRaises(ValidationError):
            Class.objects.create(name="History Class")

    def test_class_without_grade(self) -> None:
        class_obj: Class = Class.objects.create(
            teacher=self.teacher, name="English Class"
        )
        self.assertIsNone(class_obj.grade)

    def test_add_student_to_class(self) -> None:
        class_obj: Class = Class.objects.create(
            teacher=self.teacher, name="Physics Class"
        )
        class_obj.students.add(self.student)
        self.assertIn(self.student, class_obj.students.all())

    def test_class_name_max_length(self) -> None:
        long_name: str = "x" * 129
        with self.assertRaises(ValidationError):
            class_obj = Class(teacher=self.teacher, name=long_name)
            class_obj.full_clean()

    def test_class_name_blank(self) -> None:
        with self.assertRaises(ValidationError):
            class_obj = Class(teacher=self.teacher, name="")
            class_obj.full_clean()

    def test_class_name_null(self) -> None:
        with self.assertRaises(ValidationError):
            class_obj = Class(teacher=self.teacher)
            class_obj.full_clean()

    def test_cascade_delete_teacher(self) -> None:
        class_obj: Class = Class.objects.create(
            teacher=self.teacher, name="Chemistry Class"
        )
        self.teacher.delete()
        self.assertFalse(Class.objects.filter(pk=class_obj.pk).exists())

    def test_grade_set_null_on_delete(self) -> None:
        class_obj: Class = Class.objects.create(
            teacher=self.teacher, name="Biology Class", grade=self.grade
        )
        # delete student before deleting grade
        # since grade.on_delete is PROTECTED
        self.student.delete()
        self.grade.delete()
        class_obj.refresh_from_db()
        self.assertIsNone(class_obj.grade)

    def test_all_students_same_grade(self) -> None:
        class_obj: Class = Class.objects.create(
            teacher=self.teacher, name="Geography Class", grade=self.grade
        )
        class_obj.students.add(self.student)
        user: User = User.objects.create_user(
            email="user2", username="user2", password="user2", role=User.Role.STUDENT
        )
        grade: Grade = Grade.objects.create(
            name="Second Grade", stage=self.stage, order_in_stage=2
        )
        student2: Student = Student.objects.create(user=user, grade=grade)
        with self.assertRaises(
            ValidationError, msg="All students must be in the same grade"
        ):
            class_obj.students.add(student2)
            class_obj.save()

    def test_all_students_same_grade_as_class(self) -> None:
        class_obj: Class = Class.objects.create(
            teacher=self.teacher, name="Geography Class", grade=self.grade
        )
        class_obj.students.add(self.student)
        user: User = User.objects.create_user(
            email="user2", username="user2", password="user2", role=User.Role.STUDENT
        )
        grade: Grade = Grade.objects.create(
            name="Second Grade", stage=self.stage, order_in_stage=2
        )
        student2: Student = Student.objects.create(user=user, grade=grade)
        with self.assertRaises(
            ValidationError, msg="All students must be in the same grade as the class"
        ):
            class_obj.students.add(student2)
            class_obj.save()

    def test_max_students_reached(self) -> None:
        class_obj: Class = Class.objects.create(
            teacher=self.teacher, name="Geography Class", grade=self.grade
        )
        for i in range(10):
            user = User.objects.create_user(
                email=f"user{i}",
                username=f"user{i}",
                password=f"user{i}",
                role=User.Role.STUDENT,
            )
            student = Student.objects.create(user=user, grade=self.grade)
            class_obj.students.add(student)
        with self.assertRaises(
            ValidationError, msg="You have reached the maximum number of students"
        ):
            user = User.objects.create_user(
                email="user11",
                username="user11",
                password="user11",
                role=User.Role.STUDENT,
            )
            grade: Grade = Grade.objects.create(
                name="Grade 11", stage=self.stage, order_in_stage=11
            )
            student = Student.objects.create(user=user, grade=grade)
            class_obj.students.add(student)
            class_obj.save()


class ClassSignalTestCase(TestCase):
    """a test case for classes signals"""

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
        self.subject: Subject = Subject.objects.create(name="Math")
        self.user_teacher: User = User.objects.create_user(
            email="teacher@tmail.com",
            username="teacher",
            password="teacherPass",
            role=User.Role.TEACHER,
        )
        self.teacher: Teacher = Teacher.objects.create(
            user=self.user_teacher, subject=self.subject, max_students=10
        )
        self.grade: Grade = Grade.objects.create(
            stage=self.stage, name="First grade", order_in_stage=1
        )
        self.students: list[Student] = []
        for i in range(10):
            user = User.objects.create_user(
                email=f"user{i}",
                username=f"user{i}",
                password=f"user{i}",
                role=User.Role.STUDENT,
            )
            self.students.append(Student.objects.create(user=user, grade=self.grade))

    def test_max_student_number_after_creating_class(self) -> None:
        Class.objects.create(
            teacher=self.teacher,
            name="class 1",
            grade=self.grade,
        )
        self.assertEqual(self.teacher.max_students, self.teacher.available_students)

    def test_max_student_number_after_adding_students(self) -> None:
        class_obj: Class = Class.objects.create(
            teacher=self.teacher,
            name="class 1",
            grade=self.grade,
        )
        class_obj.students.add(*self.students[:5])
        class_obj.save()
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.available_students, 10 - 5)
        class_obj.students.add(*self.students[5:])
        class_obj.save()
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.available_students, 0)

    def test_exeeding_max_students_number(self) -> None:
        class_obj: Class = Class.objects.create(
            teacher=self.teacher,
            name="class 1",
            grade=self.grade,
        )
        class_obj.students.add(*self.students)
        class_obj.save()
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.max_students, 10)
        new_user: User = User.objects.create_user(
            email="user11",
            username="user11",
            password="user11",
            role=User.Role.STUDENT,
        )
        new_student: Student = Student.objects.create(user=new_user, grade=self.grade)
        with self.assertRaises(
            ValidationError,
            msg="Cannot add 1 students. Teacher can only accept 0 more students.",
        ):
            class_obj.students.add(new_student)
