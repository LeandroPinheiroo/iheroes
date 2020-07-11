from functools import partial
from operator import itemgetter

import pytest
from pytest_factoryboy import register

from tests.factories.entity_factories import (
    CreateHeroDtoFactory,
    HeroFactory,
    UpdateHeroDtoFactory,
    UserFactory,
)
from tests.factories.model_factories import insert_hero, insert_user
from tests.factories.utils import make_many
from tests.utils.auth import auth_headers

factories = [CreateHeroDtoFactory, HeroFactory, UserFactory, UpdateHeroDtoFactory]

for factory in factories:
    register(factory)


@pytest.fixture(name="make_create_hero_dto")
def make_create_hero_dto_fixture(create_hero_dto_factory):
    return lambda **override: create_hero_dto_factory(**override)


@pytest.fixture(name="make_hero")
def make_hero_fixture(hero_factory):
    return lambda **override: hero_factory(**override)


@pytest.fixture(name="make_heroes")
def make_heroes_fixture(hero_factory):
    return partial(make_many, hero_factory)


@pytest.fixture(name="make_update_hero_dto")
def make_update_hero_dto_fixture(update_hero_dto_factory):
    return lambda **override: update_hero_dto_factory(**override)


@pytest.fixture(name="make_user")
def make_user_fixture(user_factory):
    return lambda **override: user_factory(**override)


@pytest.mark.integration
class TestCreate:
    def test_success(self, test_client, logged_user, make_create_hero_dto):
        dto = make_create_hero_dto()
        with test_client as client:
            response = client.post(
                "/hero", json=dto.dict(), headers=auth_headers(logged_user.access_token)
            )
        assert response.status_code == 201

        getter = itemgetter("user_id", "name", "nickname", "power_class", "location")
        assert getter(response.json()) == getter(
            {**dto.dict(), "user_id": logged_user.user.id}
        )

    def test_conflict(self, test_client, logged_user, make_hero, make_create_hero_dto):
        hero = make_hero(user_id=logged_user.user.id)
        insert_hero(hero.dict())
        dto = make_create_hero_dto(name=hero.name, nickname=hero.nickname)

        with test_client as client:
            response = client.post(
                "/hero", json=dto.dict(), headers=auth_headers(logged_user.access_token)
            )
        assert response.status_code == 409
        assert response.json() == {
            "detail": {
                "msg": "hero already exists",
                "type": "conflict_error.not_unique",
            }
        }

    def test_validation_error(self, test_client, logged_user):
        with test_client as client:
            response = client.post(
                "/hero", json={}, headers=auth_headers(logged_user.access_token)
            )
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "loc": ["body", "dto", "nickname"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "dto", "power_class"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
                {
                    "loc": ["body", "dto", "location"],
                    "msg": "field required",
                    "type": "value_error.missing",
                },
            ]
        }

    def test_unauthenticated(self, test_client):
        with test_client as client:
            response = client.post("/hero")
        assert response.status_code == 401


@pytest.mark.integration
class TestIndex:
    def test_success(self, test_client, logged_user, make_user, make_heroes):
        other_user = make_user()
        insert_user(other_user.dict())
        heroes = [
            hero.dict()
            for hero in [
                *make_heroes(10, user_id=logged_user.user.id),
                *make_heroes(10, user_id=other_user.id),
            ]
        ]
        insert_hero(heroes)

        with test_client as client:
            response = client.get(
                "/hero", headers=auth_headers(logged_user.access_token)
            )
        assert response.status_code == 200

        response_body = response.json()
        assert len(response_body) == len(heroes)
        for hero in response_body:
            assert hero in heroes

    def test_unauthenticated(self, test_client):
        with test_client as client:
            response = client.get("/hero/index")
        assert response.status_code == 401


@pytest.mark.integration
class TestIndexByUser:
    def test_success(self, test_client, logged_user, make_user, make_heroes):
        other_user = make_user()
        insert_user(other_user.dict())
        heroes = [
            hero.dict()
            for hero in [
                *make_heroes(10, user_id=logged_user.user.id),
                *make_heroes(10, user_id=other_user.id),
            ]
        ]
        insert_hero(heroes)

        with test_client as client:
            response = client.get(
                "/hero/me", headers=auth_headers(logged_user.access_token)
            )

        assert response.status_code == 200

        response_body = response.json()
        cond = itemgetter("id")
        user_heroes = [
            hero for hero in heroes if hero["user_id"] == logged_user.user.id
        ]
        assert sorted(response_body, key=cond) == sorted(user_heroes, key=cond)

    def test_unauthenticated(self, test_client):
        with test_client as client:
            response = client.get("/hero/index")
        assert response.status_code == 401


@pytest.mark.integration
class TestShow:
    def test_success(self, test_client, logged_user, make_hero):
        id_ = 1
        hero = make_hero(id=id_, user_id=logged_user.user.id)
        insert_hero(hero.dict())

        with test_client as client:
            response = client.get(
                f"/hero/{id_}", headers=auth_headers(logged_user.access_token)
            )
        assert response.status_code == 200
        assert response.json() == hero.dict()

    def test_not_found(self, test_client, logged_user):
        with test_client as client:
            response = client.get(
                "/hero/1", headers=auth_headers(logged_user.access_token)
            )
        assert response.status_code == 404

    def test_from_other_user(self, test_client, logged_user, make_user, make_hero):
        other_user = make_user()
        insert_user(other_user.dict())

        id_ = 1
        hero = make_hero(id=id_, user_id=other_user.id)
        insert_hero(hero.dict())

        with test_client as client:
            response = client.get(
                f"/hero/{id_}", headers=auth_headers(logged_user.access_token)
            )
        assert response.status_code == 404

    def test_unauthenticated(self, test_client):
        with test_client as client:
            response = client.get("/hero/index")
        assert response.status_code == 401


@pytest.mark.integration
class TestUpdate:
    def test_success(self, test_client, logged_user, make_hero, make_update_hero_dto):
        id_ = 1
        hero = make_hero(id=id_, user_id=logged_user.user.id)
        insert_hero(hero.dict())

        dto = make_update_hero_dto()
        with test_client as client:
            response = client.put(
                f"/hero/{id_}",
                headers=auth_headers(logged_user.access_token),
                json=dto.dict(),
            )
        assert response.status_code == 200
        assert response.json() == {**hero.dict(), **dto.dict()}

    def test_conflict(self, test_client, logged_user, make_hero, make_update_hero_dto):
        id_ = 1
        hero = make_hero(id=id_, user_id=logged_user.user.id)
        other_hero = make_hero(user_id=logged_user.user.id)
        insert_hero([hero.dict(), other_hero.dict()])

        dto = make_update_hero_dto(name=other_hero.name, nickname=other_hero.nickname)
        with test_client as client:
            response = client.put(
                f"/hero/{id_}",
                headers=auth_headers(logged_user.access_token),
                json=dto.dict(),
            )
        assert response.status_code == 409
        assert response.json() == {
            "detail": {
                "msg": "hero already exists",
                "type": "conflict_error.not_unique",
            }
        }

    def test_not_found(self, test_client, logged_user, make_update_hero_dto):
        dto = make_update_hero_dto()
        with test_client as client:
            response = client.put(
                "/hero/1",
                headers=auth_headers(logged_user.access_token),
                json=dto.dict(),
            )
        assert response.status_code == 404

    def test_validation_error(self, test_client, logged_user):
        with test_client as client:
            response = client.put(
                "/hero/1",
                headers=auth_headers(logged_user.access_token),
                json={
                    "name": [],
                    "nickname": [],
                    "power_class": "over 9000",
                    "location": "brazil",
                },
            )
        assert response.status_code == 422
        assert response.json() == {
            "detail": [
                {
                    "loc": ["body", "dto", "name"],
                    "msg": "str type expected",
                    "type": "type_error.str",
                },
                {
                    "loc": ["body", "dto", "nickname"],
                    "msg": "str type expected",
                    "type": "type_error.str",
                },
                {
                    "ctx": {"enum_values": ["S", "A", "B", "C"]},
                    "loc": ["body", "dto", "power_class"],
                    "msg": "value is not a valid enumeration member; permitted: 'S', "
                    "'A', 'B', 'C'",
                    "type": "type_error.enum",
                },
                {
                    "loc": ["body", "dto", "location"],
                    "msg": "value is not a valid dict",
                    "type": "type_error.dict",
                },
            ]
        }

    def test_unauthenticated(self, test_client):
        with test_client as client:
            response = client.put("/hero/1")
        assert response.status_code == 401


@pytest.mark.integration
class TestDelete:
    def test_found(self, test_client, logged_user, make_hero):
        id_ = 1
        hero = make_hero(id=id_, user_id=logged_user.user.id)
        insert_hero(hero.dict())

        with test_client as client:
            response = client.delete(
                "/hero/1", headers=auth_headers(logged_user.access_token)
            )
        assert response.status_code == 204

    def test_not_found(self, test_client, logged_user):
        with test_client as client:
            response = client.delete(
                "/hero/1", headers=auth_headers(logged_user.access_token)
            )
        assert response.status_code == 404

    def test_unauthenticated(self, test_client):
        with test_client as client:
            response = client.delete("/hero/1")
        assert response.status_code == 401
