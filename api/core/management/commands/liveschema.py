from datetime import date
from random import randint

from api.leagues import factories, models
from django.core.management.base import BaseCommand, CommandError
from django.utils import autoreload


def foo():
    print("hi")

class Command(BaseCommand):

    def handle(self, *args, **options):
        pass
        # TODO: autoreload.run_with_reloader(foo, args=None, kwargs=None)
