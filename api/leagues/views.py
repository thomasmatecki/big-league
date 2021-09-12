from dataclasses import dataclass
from datetime import date

from api.core.rest import IsAuthenticatedOrCreateOnly
from api.leagues import models, serializers
from django.contrib.auth.models import AbstractBaseUser
from rest_framework import generics, viewsets


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = models.Player.objects.all()
    serializer_class = serializers.PlayerSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer


class SeasonViewSet(viewsets.ModelViewSet):
    queryset = models.Season.objects.all()
    serializer_class = serializers.SeasonSerializer


class LeagueViewSet(viewsets.ModelViewSet):
    queryset = models.League.objects.all()
    serializer_class = serializers.LeagueSerializer


class ProfileViewSet(
    generics.RetrieveUpdateAPIView, generics.CreateAPIView, viewsets.GenericViewSet
):

    serializer_class = serializers.ProfileSerializer
    permission_classes = [IsAuthenticatedOrCreateOnly]

    def get_object(self):
        player = models.Player.objects.get(user=self.request.user)
        date_joined = player.user.date_joined.date()
        return serializers.Profile(
            pk=player.pk, date_joined=date_joined, player=player, user=player.user
        )


class MatchViewSet(viewsets.ModelViewSet):
    queryset = models.Match.objects.all()
    serializer_class = serializers.MatchSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    # TODO: Filter to requesting user
    queryset = (
        models.Schedule.objects.select_related("team", "match", "match__location")
        .prefetch_related("match__teams")
        .all()
    )
    serializer_class = serializers.ScheduleSerializer
