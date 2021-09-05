from django.utils import autoreload
from rest_framework.management.commands import generateschema


class Command(generateschema.Command):
    def handle(self, *args, **options):
        # self.stdout("This command auto reloads. No need to restart...")
        autoreload.run_with_reloader(super().handle, *args, **options)
