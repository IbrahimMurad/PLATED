import nested_admin
from django.contrib import admin

from .models import Answer, Question


# make answers nestable in questions
class AnswerInline(nested_admin.NestedTabularInline):
    model = Answer
    extra = 0


# nest answers in questions
class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ["body", "difficulty", "lesson"]


# nest answers in nestable questions
class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    inlines = [AnswerInline]
    extra = 0


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
