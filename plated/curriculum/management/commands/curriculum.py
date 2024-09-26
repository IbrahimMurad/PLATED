from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "For usage insteade of shell"

    def handle(self, *args, **kwargs):
        pass
