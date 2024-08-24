from django.contrib import admin
from .models import Subject, Unit, Chapter, Lesson
from questions.admin import QuestionInline
import nested_admin


# nest related questions with the nested answers to the lesson admin page
# show only title, id, and chapter title in the lessons list admin page
# also add a filter as a side bar to filter lessons by chapter
# group some fields in advanced options and collapse by default 
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


# add related lessons to chapter admin page
class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 0


# also, show only the chapter number and unit in the chapters list admin page
class ChapterAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ['title', 'number', 'unit']


# add related chapters to subject admin page
class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 0


class UnitAdmin(admin.ModelAdmin):
    inlines = [ChapterInline]


# add related units to subject admin page
class UnitInline(admin.TabularInline):
    model = Unit
    extra = 0


class SubjectAdmin(admin.ModelAdmin):
    inlines = [UnitInline]


admin.site.register(Subject, SubjectAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Lesson, LessonAdmin)
