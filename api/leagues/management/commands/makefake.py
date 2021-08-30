from datetime import date
from random import randint

from api.leagues import factories, models
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create Fake League Data"

    def handle(self, *args, **options):
        league = models.League.objects.create(name="Social Flag Football")
        season = models.Season.objects.create(
            league=league,
            name="Fall 2022",
            released=True,
            start_date=date(2022, 8, 1),
            end_date=date(2022, 9, 30),
        )

        for _ in range(13):
            players = [factories.PlayerFactory() for _ in range(randint(9, 15))]
            factories.TeamFactory(season=season, players=players)
