from django.urls import path
from .views import lesson_exam, solved_exam, exam_list


urlpatterns = [
    path('', exam_list, name='exams'),
    path('<int:id>/solved/', solved_exam, name='solved-exam'),
    path('<int:id>/', lesson_exam, name='lesson-exam'),
    path('<int:id>/delete/', lesson_exam, name='delete-exam'),
]
