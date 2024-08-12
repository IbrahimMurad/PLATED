from django import forms
from django.contrib import admin
from .models import Question, Answer
import nested_admin


class AnswerInline(nested_admin.NestedTabularInline):
    model = Answer
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ['body', 'difficulty', 'lesson']


class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    inlines = [AnswerInline]
    extra = 0


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
