from django.contrib import admin
from .models import Subject, Unit, Chapter, Lesson


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

class ChapterAdmin(admin.ModelAdmin):
    inlines = [LessonInline]

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1

class UnitAdmin(admin.ModelAdmin):
    inlines = [ChapterInline]

class UnitInline(admin.TabularInline):
    model = Unit
    extra = 1

class SubjectAdmin(admin.ModelAdmin):
    inlines = [UnitInline]

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Lesson)
