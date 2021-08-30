from django.db import models

# Create your models here.


class League(models.Model):
    name = models.CharField(max_length=100)


class Season(models.Model):
    name = models.CharField(max_length=100)
    league = models.ForeignKey(to="leagues.League", on_delete=models.DO_NOTHING)
    released = models.BooleanField(
        help_text="Is the schedule for this season visible?", default=False
    )
    start_date = models.DateField()
    end_date = models.DateField()


class Player(models.Model):
    display_name = models.CharField(max_length=100)
    user = models.OneToOneField(null=True, to="auth.User", on_delete=models.DO_NOTHING)
    email_confirmed = models.BooleanField(default=False)

    class Manager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().annotate(email=models.F("user__email"))

    objects = Manager()


class Team(models.Model):
    name = models.CharField(max_length=100)
    captain = models.ForeignKey(
        to="leagues.Player", null=True, on_delete=models.DO_NOTHING
    )
    season = models.ForeignKey(
        to="leagues.Season", related_name="teams", on_delete=models.DO_NOTHING
    )
    players = models.ManyToManyField(to="leagues.Player", related_name="teams")

    def __str__(self):
        return f"{self.name} ({self.pk})"

    class Meta:
        ordering = ["id"]


class Location(models.Model):
    name = models.CharField(max_length=100)


class Schedule(models.Model):
    game = models.ForeignKey(to="leagues.Game", on_delete=models.CASCADE)
    team = models.ForeignKey(to="leagues.Team", on_delete=models.CASCADE)
    away = models.BooleanField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["game", "away"],
                name="home_or_away",
            ),
            models.UniqueConstraint(
                fields=["game", "team"],
                name="vs_other_team",
            ),
        ]


class Game(models.Model):
    datetime = models.DateTimeField()
    season = models.ForeignKey(to="leagues.Season", on_delete=models.DO_NOTHING)
    teams = models.ManyToManyField(to="leagues.Team", through="leagues.Schedule")
    location = models.ForeignKey(to="leagues.Location", on_delete=models.DO_NOTHING)
