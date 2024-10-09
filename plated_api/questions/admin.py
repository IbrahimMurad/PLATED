from django.contrib import admin
from questions.models import Choice, Question, Type

admin.site.register(Choice)
admin.site.register(Type)
admin.site.register(Question)
