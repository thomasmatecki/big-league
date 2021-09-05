from dataclasses import dataclass
from typing import Union

from api.leagues import models, serializers
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
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


@dataclass
class Profile:
    user: Union[AbstractBaseUser, AnonymousUser]
    player: models.Player


class ProfileViewSet(generics.RetrieveUpdateAPIView, viewsets.GenericViewSet):
    def get_object(self):
        player = models.Player.objects.get(user=self.request.user)
        return Profile(user=self.request.user, player=player)

    serializer_class = serializers.ProfileSerializer
