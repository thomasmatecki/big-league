from api.core.rest import IsAuthenticatedOrCreateOnly
from api.leagues import filters, models, serializers
from django.db.models import F
from django.shortcuts import get_object_or_404
from django_filters import FilterSet
from rest_framework import generics, mixins, viewsets
from rest_framework.renderers import TemplateHTMLRenderer


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = models.Player.objects.all()
    serializer_class = serializers.PlayerSerializer


class TeamViewSet(viewsets.ModelViewSet):
    queryset = models.Team.objects.all()
    serializer_class = serializers.TeamSerializer
    filterset_class = filters.DefaultFilterSet


class SeasonViewSet(viewsets.ModelViewSet):
    queryset = models.Season.objects.all()
    serializer_class = serializers.SeasonSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "season-list.html"

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


class AttendanceViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = serializers.AttendanceSerializer

    class filterset_class(FilterSet):
        match_id = filters.NumberInFilter(field_name="match_id", lookup_expr="in")

        class Meta:
            model = models.Attendance
            fields = ("match_id",)

    def get_queryset(self):
        queryset = (
            models.Player.objects.filter(teams__match__isnull=False)
            .values(
                player_id=F("id"),
                match_id=F("teams__match"),
                attending=F("attendance__attending"),
            )
            .order_by("player_id")
        )

        queryset.model = models.Attendance

        return queryset

    def get_serializer(self, *args, **kwargs):
        if args:
            args = ((models.Attendance(**kwargs) for kwargs in args[0]), *args[1:])

        return super().get_serializer(*args, **kwargs)
