from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create user groups for the project"

    def handle(self, *args, **kwargs):
        group_names = ["Student", "Teacher", "Admin"]

        for group_name in group_names:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f"Created group: {group_name}")
            else:
                self.stdout.write(f"Group {group_name} already exists")
