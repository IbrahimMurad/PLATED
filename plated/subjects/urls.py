from django.urls import path
from .views import (
    subjects_view,
    units_view,
    chapters_view,
    lessons_view,
    lesson_details_view,
    tag_lesson_view
)

urlpatterns = [
    path('', subjects_view, name='subjects-list'),
    path('<int:id>/', units_view, name='units-list'),
    path('unit/<int:id>/', chapters_view, name='chapters-list'),
    path('chapter/<int:id>/', lessons_view, name='lessons-list'),
    path('lesson/<int:id>/', lesson_details_view, name='lesson-details'),
    path('lesson/<int:id>/tag/', tag_lesson_view, name='tag-lesson'),
]
