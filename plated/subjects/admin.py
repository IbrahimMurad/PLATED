from django.contrib import admin
from .models import Subject, Unit, Chapter, Lesson


class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'chapter']
    list_filter = ['chapter']

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

class ChapterAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ['title', 'number', 'unit']

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
admin.site.register(Lesson, LessonAdmin)
