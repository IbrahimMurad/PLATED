from django.core.management.base import BaseCommand

from subjects.models import Subject


class Command(BaseCommand):
    help = "For usage insteade of shell"

    def handle(self, *args, **kwargs):
        for subject in Subject.objects.values():
            print(subject)
