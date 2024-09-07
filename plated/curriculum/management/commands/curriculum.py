from django.core.management.base import BaseCommand
from curriculum.models import Curriculum, Grade, Semester

class Command(BaseCommand):
    help = 'For usage insteade of shell'

    def handle(self, *args, **kwargs):
        pass
