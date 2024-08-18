from django.urls import path
from .views import exam, solved_exam, exam_list, generate_exam, delete_exam


urlpatterns = [
    path('', exam_list, name='exams'),
    path('create/', generate_exam, name='generate-exam'),
    path('<int:id>/solved/', solved_exam, name='solved-exam'),
    path('<int:id>/delete/', delete_exam, name='delete-exam'),
    path('<int:id>/', exam, name='exam'),
]
