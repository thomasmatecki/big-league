from django.db import models


# Create your models here.
class League(models.Model):
    name = models.CharField(max_length=100)


class Season(models.Model):
    name = models.CharField(max_length=100)
    league = models.ForeignKey(to="leagues.League", on_delete=models.DO_NOTHING)
    released = models.BooleanField(help_text="Is the schedule for this league visible?")
    start_date = models.DateField()
    end_date = models.DateField()


class Player(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(null=True, to="auth.User", on_delete=models.DO_NOTHING)


class Team(models.Model):
    name = models.CharField(max_length=100)
    players = models.ManyToManyField(
        to="leagues.Player",
    )

class Location(models.Model):
    name = models.CharField(max_length=100)


class Game(models.Model):
    datetime = models.DateTimeField()
    season = models.ForeignKey(to="leagues.Season", on_delete=models.DO_NOTHING)
    teams = models.ManyToManyField(to="leagues.Team")
    location = models.ForeignKey(to="leagues.Location", on_delete=models.DO_NOTHING)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(teams__count=2), name="teams_eq_2")
        ]
