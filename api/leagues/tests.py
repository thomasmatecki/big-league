import pytest
from rest_framework import exceptions

from api.leagues.serializers import PlayerSerializer


def test_email_required():
    serializer = PlayerSerializer(data={"first_name": "Thomas", "last_name": "Thomas"})
    with pytest.raises(exceptions.ValidationError):
        serializer.is_valid(raise_exception=True)


def test_can_set_email():
    serializer = PlayerSerializer(
        data={
            "first_name": "Thomas",
            "last_name": "Thomas",
            "password": "wab2bb2bb",
            "email": "thomas@email.com",
        }
    )
    assert serializer.is_valid(raise_exception=True)


def test_cannot_update_email(player):
    serializer = PlayerSerializer(
        instance=player,
        data={
            "first_name": "Thomas",
            "last_name": "Thomas",
            "email": "something@email.com",
        },
        partial=True,
    )
    with pytest.raises(exceptions.ValidationError):
        serializer.is_valid(raise_exception=True)


def test_valid():
    serializer = PlayerSerializer(
        data={
            "first_name": "Thomas",
            "last_name": "Thomas",
            "password": "wab2bb2bb",
            "email": "thomas@matecki.email",
        }
    )
    assert serializer.is_valid(raise_exception=True)
