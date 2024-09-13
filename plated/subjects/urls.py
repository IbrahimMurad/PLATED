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
    path('<uuid:id>/', units_view, name='units-list'),
    path('unit/<uuid:id>/', chapters_view, name='chapters-list'),
    path('chapter/<uuid:id>/', lessons_view, name='lessons-list'),
    path('lesson/<uuid:id>/', lesson_details_view, name='lesson-details'),
    path('lesson/<uuid:id>/tag/', tag_lesson_view, name='tag-lesson'),
]
