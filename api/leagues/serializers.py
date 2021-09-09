from api.core.rest import CreateOnlyValidator
from api.leagues import models
from django.contrib.auth import get_user_model
from rest_framework import exceptions, serializers, validators


class LeagueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.League
        fields = ["id", "url", "name"]


class HyperlinkedSeasonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Season
        fields = ["id", "url", "name"]


class HyperLinkedTeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Team
        fields = ["id", "url", "name"]


class SeasonSerializer(HyperlinkedSeasonSerializer):
    league = LeagueSerializer()
    teams = HyperLinkedTeamSerializer(many=True)

    class Meta:
        model = models.Season
        fields = ["id", "url", "name", "league", "start_date", "end_date", "teams"]


class HyperLinkedPlayerSerializer(serializers.HyperlinkedModelSerializer):
    display_name = serializers.CharField(required=False)

    class Meta:
        model = models.Player
        fields = [
            "id",
            "url",
            "display_name",
        ]


class HyperlinkedTeamSerializer(serializers.HyperlinkedModelSerializer):
    players = HyperLinkedPlayerSerializer(required=False, many=True, read_only=True)
    captain = HyperLinkedPlayerSerializer()
    season = HyperlinkedSeasonSerializer()
    league = LeagueSerializer(source="season.league")

    class Meta:
        model = models.Team
        fields = ["id", "url", "name"]


class TeamSerializer(HyperLinkedTeamSerializer):
    players = HyperLinkedPlayerSerializer(required=False, many=True, read_only=True)
    captain = HyperLinkedPlayerSerializer()
    season = HyperlinkedSeasonSerializer()
    league = LeagueSerializer(source="season.league")

    class Meta:
        model = models.Team
        fields = [
            "id",
            "url",
            "name",
            "league",
            "season",
            "captain",
            "players",
        ]


class PlayerSerializer(HyperLinkedPlayerSerializer):
    email = serializers.EmailField(
        source="user.email",
        default="",
        validators=[
            CreateOnlyValidator(),
            validators.UniqueValidator(
                queryset=models.Player.objects.all(),
                message="This email is already registered.",
            ),
        ],
    )
    password = serializers.CharField(
        source="user.password", required=True, write_only=True
    )
    first_name = serializers.CharField(write_only=True, source="user.first_name")
    last_name = serializers.CharField(write_only=True, source="user.last_name")
    teams = HyperLinkedTeamSerializer(required=False, read_only=True, many=True)
    team_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        source="teams",
        required=False,
        queryset=models.Team.objects.all(),
    )

    def create(self, validated_data):
        user_data = validated_data.pop("user")

        validated_data["display_name"] = "{first_name} {last_name}".format_map(
            user_data
        )

        User = get_user_model()

        # In case a user exists that is not yet associated with a player.
        user = User.objects.filter(email=["email"]).first() or User.objects.create_user(
            username=user_data["email"], **user_data
        )

        validated_data["user"] = user

        return super().create(validated_data)

    class Meta:
        model = models.Player
        fields = [
            "id",
            "url",
            "email",
            "password",
            "last_name",
            "first_name",
            "display_name",
            "teams",
            "team_ids",
        ]


class ProfileSerializer(serializers.Serializer):
    display_name = serializers.CharField(source="player.display_name")


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Match
        exclude = []


class ScheduleSerializer(serializers.ModelSerializer):
    team = HyperLinkedTeamSerializer()
    opponent = HyperLinkedTeamSerializer()
    datetime = serializers.DateTimeField(source="match.datetime")
    location = serializers.CharField(source="match.location.name")

    class Meta:
        model = models.Schedule
        exclude = ["match"]
