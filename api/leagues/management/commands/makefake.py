from datetime import date, datetime
from random import randint

from django.core.management.base import BaseCommand

from api.leagues import factories, models


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
        teams = []

        for team in range(13):
            players = [factories.PlayerFactory() for _ in range(randint(9, 15))]
            teams.append(factories.TeamFactory(season=season, players=players))

        location = models.Location.objects.create(name="Long Branch Park")
        match = models.Match.objects.create(
            season=season, location=location, datetime=datetime(2022, 8, 1, hour=11)
        )

        models.Schedule.objects.create(match=match, away=True, team=teams[0])
        models.Schedule.objects.create(match=match, away=False, team=teams[1])
