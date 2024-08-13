from django.contrib import admin
from .models import Subject, Unit, Chapter, Lesson
from questions.admin import QuestionInline
import nested_admin


class LessonAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]
    list_display = ['title', 'id', 'chapter']
    list_filter = ['chapter']
    fieldsets = [
        (
            None,
            {
                'fields': ['title', 'chapter', 'grade', 'semester']
            }
        ),
        (
            'Advanced options',
            {
                'classes': ['collapse'],
                'fields': ['number', 'caption', 'cover', 'intro', 'goals', 'details', 'notes', 'required_by', 'requires'],
            },
        ),
    ]


class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0


class ChapterAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ['title', 'number', 'unit']


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 0


class UnitAdmin(admin.ModelAdmin):
    inlines = [ChapterInline]


class UnitInline(admin.TabularInline):
    model = Unit
    extra = 0


class SubjectAdmin(admin.ModelAdmin):
    inlines = [UnitInline]


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Lesson, LessonAdmin)
