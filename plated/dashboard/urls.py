from django.urls import path

from dashboard.views import (
    chapter_dashboard_view,
    lesson_dashboard_view,
    main_dashboard_view,
    subject_dashboard_view,
    unit_dashboard_view,
)

urlpatterns = [
    path("", main_dashboard_view, name="main-dashboard"),
    path("subject/", subject_dashboard_view, name="subjects-dashboard"),
    path("subject/<uuid:id>/units/", unit_dashboard_view, name="units-dashboard"),
    path("unit/<uuid:id>/chapters/", chapter_dashboard_view, name="chapters-dashboard"),
    path("chapter/<uuid:id>/lessons/", lesson_dashboard_view, name="lessons-dashboard"),
]
