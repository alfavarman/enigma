import json
import os

from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Set up predefined groups and permissions as in docs/permissions.json'

    def handle(self, *args, **kwargs):
        # path to docks folder - to refactor from abspath
        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))

        json_path = os.path.join(base_dir, 'docs', 'permissions.json')

        with open(json_path, 'r') as file:
            GROUPS_PERMISSIONS = json.load(file)

        for group_name, permissions in GROUPS_PERMISSIONS.items():
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" created'))
            else:
                self.stdout.write(self.style.WARNING(f'Group "{group_name}" already exists'))

            for codename in permissions:
                try:
                    perm = Permission.objects.get(codename=codename)
                except ObjectDoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Permission "{codename}" not found!'))
                    continue

                # Check if the group already has the permission
                if perm in group.permissions.all():
                    self.stdout.write(self.style.WARNING(f'Group "{group_name}" already has permission "{codename}"'))
                else:
                    group.permissions.add(perm)
                    self.stdout.write(self.style.SUCCESS(f'Permission "{codename}" added to group "{group_name}"'))

