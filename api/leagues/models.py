from __future__ import annotations

from django.db import models


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
    biography = models.TextField(default="")
    image = models.ImageField(null=True)

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
    team = models.ForeignKey(to="leagues.Team", on_delete=models.CASCADE)
    match = models.ForeignKey(to="leagues.Match", on_delete=models.CASCADE)
    away = models.BooleanField()

    @property
    def opponent(self) -> Team | None:
        if self.pk:
            # TODO: Is this executing add'l SQL even in prefetching in the view?
            return self.match.teams.exclude(pk=self.pk).first()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["match", "away"],
                name="home_or_away",
            ),
            models.UniqueConstraint(
                fields=["match", "team"],
                name="vs_other_team",
            ),
        ]


class Match(models.Model):
    datetime = models.DateTimeField()
    season = models.ForeignKey(to="leagues.Season", on_delete=models.DO_NOTHING)
    teams = models.ManyToManyField(to="leagues.Team", through="leagues.Schedule")
    location = models.ForeignKey(to="leagues.Location", on_delete=models.DO_NOTHING)

    @property
    def name(self) -> str:
        return "{0} vs {1}".format(*self.teams.values_list("name", flat=True))


class Attendance(models.Model):
    match = models.ForeignKey(to="leagues.Match", on_delete=models.CASCADE)
    player = models.ForeignKey(to="leagues.Player", on_delete=models.CASCADE)
    attending = models.BooleanField(null=False)

    class Meta:
        constraints = []
