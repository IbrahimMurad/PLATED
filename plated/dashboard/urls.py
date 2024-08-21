from django.urls import path
from .views import (
    main_dashboard_view,
    subject_dashboard_view,
    unit_dashboard_view,
    chapter_dashboard_view,
    lesson_dashboard_view,
    )


urlpatterns = [
    path('subjects/', subject_dashboard_view, name='subjects-dashboard'),
    path('units/', unit_dashboard_view, name='units-dashboard'),
    path('chapters/', chapter_dashboard_view, name='chapters-dashboard'),
    path('lessons/', lesson_dashboard_view, name='lessons-dashboard'),
    path('', main_dashboard_view, name='main-dashboard'),
]
