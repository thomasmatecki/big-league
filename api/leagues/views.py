from api.core.rest import IsAuthenticatedOrCreateOnly
from api.leagues import filters, models, serializers
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = models.Player.objects.all()
    serializer_class = serializers.PlayerSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer
    filterset_class = filters.F


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

    def get_queryset(self):
        if self.request:
            return models.Player.objects.filter(user=self.request.user)
        return models.Player.objects.none()

    def get_object(self):
        queryset = self.get_queryset()
        player = get_object_or_404(queryset)
        # May raise a permission denied
        self.check_object_permissions(self.request, player)

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
