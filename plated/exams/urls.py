from django.urls import path
from .views import (
    exam,
    solved_exam,
    exam_list,
    generate_exam,
    delete_exam,
    get_focus_instances,
)


urlpatterns = [
    path('', exam_list, name='exams'),
    path('create/', generate_exam, name='generate-exam'),
    path('<uuid:id>/solved/', solved_exam, name='solved-exam'),
    path('<uuid:id>/delete/', delete_exam, name='delete-exam'),
    path('<uuid:id>/', exam, name='exam'),
    path('get-focus-instances/', get_focus_instances, name='get-focus-instances'),
]
