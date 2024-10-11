from django.contrib import admin
from users.models import Student, Teacher, User

admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Student)
