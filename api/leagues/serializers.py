from dataclasses import dataclass
from datetime import date

from api.core.rest import CreateOnlyValidator
from api.core.serializers import HyperLinkedObjectSerializer
from api.leagues import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from rest_framework import serializers, validators


class LeagueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.League
        fields = ["id", "url", "name"]


class SeasonSerializer(serializers.HyperlinkedModelSerializer):
    league = HyperLinkedObjectSerializer(model=models.League)
    teams = HyperLinkedObjectSerializer(model=models.Team, many=True)

    class Meta:
        model = models.Season
        fields = ["id", "url", "name", "league", "start_date", "end_date", "teams"]


class TeamSerializer(serializers.HyperlinkedModelSerializer):

    league = LeagueSerializer(source="season.league")
    season = HyperLinkedObjectSerializer(model=models.Season)
    players = HyperLinkedObjectSerializer(
        model=models.Player,
        sources={"name": "display_name"},
        required=False,
        many=True,
        read_only=True,
    )
    captain = HyperLinkedObjectSerializer(
        model=models.Player,
        sources={"name": "display_name"},
    )

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


def create_user_for_player(user_data: dict):

    user_model = get_user_model()

    # In case a user exists that is not yet associated with a player.
    user = user_model.objects.filter(
        email=["email"]
    ).first() or user_model.objects.create_user(
        username=user_data["email"], **user_data
    )

    return user


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    email = serializers.EmailField(
        write_only=True,
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
    first_name = serializers.CharField(write_only=True, source="user.first_name")
    last_name = serializers.CharField(write_only=True, source="user.last_name")
    teams = HyperLinkedObjectSerializer(
        model=models.Team, required=False, read_only=True, many=True
    )
    team_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        source="teams",
        required=False,
        queryset=models.Team.objects.all(),
    )

    def create(self, validated_data):
        user_data = validated_data.pop("user", {})

        validated_data["display_name"] = "{first_name} {last_name}".format_map(
            user_data
        )

        if "email" in user_data:
            user = create_user_for_player(user_data)
        else:
            user = None

        validated_data["user"] = user

        return super().create(validated_data)

    class Meta:
        model = models.Player
        fields = [
            "id",
            "url",
            "email",
            "last_name",
            "first_name",
            "display_name",
            "teams",
            "team_ids",
        ]


@dataclass
class Profile:
    pk: int
    date_joined: date
    player: models.Player
    user: AbstractBaseUser


class ProfileSerializer(serializers.Serializer):

    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")

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

    password = serializers.CharField(source="user.password", write_only=True)

    display_name = serializers.CharField(source="player.display_name", required=False)

    biography = serializers.CharField(
        source="player.biography", required=False, allow_blank=True
    )
    date_joined = serializers.DateField(read_only=True)
    image = serializers.ImageField(
        source="player.image", required=False, allow_null=True
    )

    def update(self, instance, validated_data):
        return instance

    def create(self, validated_data):
        user_data = validated_data.pop("user")

        user = create_user_for_player(user_data)

        player_data = validated_data.pop("player", {})
        player_data.setdefault(
            "display_name", "{first_name} {last_name}".format_map(user_data)
        )

        player_data["user"] = user

        player = models.Player.objects.create(**player_data)

        return Profile(
            pk=player.pk, date_joined=user.date_joined.date(), user=user, player=player
        )


class MatchSerializer(serializers.ModelSerializer):

    teams = HyperLinkedObjectSerializer(model=models.Team, many=True)

    class Meta:
        model = models.Match
        exclude = []


class ScheduleSerializer(serializers.ModelSerializer):
    team = HyperLinkedObjectSerializer(model=models.Team)
    opponent = HyperLinkedObjectSerializer(model=models.Team)
    datetime = serializers.DateTimeField(source="match.datetime")
    location = serializers.CharField(source="match.location.name")

    class Meta:
        model = models.Schedule
        exclude = ["match"]
