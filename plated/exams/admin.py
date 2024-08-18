from django.contrib import admin
from .models import Exam, StudentAnswer
from questions.models import Question

class QuestionInline(admin.TabularInline):
    model = Exam.questions.through
    extra = 0


class ExamAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


admin.site.register(Exam, ExamAdmin)    
admin.site.register(StudentAnswer)
