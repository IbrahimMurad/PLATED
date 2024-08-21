from django.urls import path
from .views import (
    main_dashboard_view,
    subject_dashboard_view,
    unit_dashboard_view,
    chapter_dashboard_view,
    lesson_dashboard_view,
    )


urlpatterns = [
    path('', main_dashboard_view, name='main-dashboard'),
    path('subject/', subject_dashboard_view, name='subjects-dashboard'),
    path('subject/<int:id>/units/', unit_dashboard_view, name='units-dashboard'),
    path('unit/<int:id>/chapters/', chapter_dashboard_view, name='chapters-dashboard'),
    path('chapter/<int:id>/lessons/', lesson_dashboard_view, name='lessons-dashboard'),
]
