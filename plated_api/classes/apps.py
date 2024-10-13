from django.apps import AppConfig


class ClassesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "classes"

    def ready(self) -> None:
        import classes.signals  # noqa: F401
