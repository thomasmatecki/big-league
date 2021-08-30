import pytest
from pytest_factoryboy import register

from api.core.factories import UserFactory
from api.leagues.factories import PlayerFactory


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):  # pylint: disable=unused-argument,invalid-name
    pass


register(PlayerFactory)
register(UserFactory)
