from api.leagues import models, serializers
from rest_framework import viewsets

# Create your views here.


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
