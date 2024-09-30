from django.contrib import admin
from grades.models.curriculum import Curriculum
from grades.models.grade import Grade
from grades.models.path import Path
from grades.models.semester import Semester
from grades.models.stage import Stage

admin.site.register(Curriculum)
admin.site.register(Path)
admin.site.register(Stage)
admin.site.register(Grade)
admin.site.register(Semester)
