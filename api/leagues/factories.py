import factory
from api.core.factories import UserFactory
from api.leagues import models
from factory.django import DjangoModelFactory


class PlayerFactory(DjangoModelFactory):
    class Meta:
        model = models.Player

    user = factory.SubFactory(UserFactory, player=None)

    display_name = factory.LazyAttribute(
        lambda p: "{user.first_name} {user.last_name}".format(user=p.user)
    )

    @factory.post_generation
    def teams(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            self.teams.add(*extracted)


class TeamFactory(DjangoModelFactory):
    class Meta:
        model = models.Team

    name = factory.Faker("catch_phrase")
    captain = factory.SubFactory(PlayerFactory)

    @factory.post_generation
    def players(self, create, extracted, **kwargs):

        self.players.add(self.captain)

        if not create:
            return
        if extracted:
            self.players.add(*extracted)
