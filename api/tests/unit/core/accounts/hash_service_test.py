import pytest
from faker import Faker

from iheroes_api.core.accounts import hash_service

fake = Faker()


@pytest.fixture(name="secret")
def secret_fixture():
    return fake.pystr()


@pytest.fixture(name="other")
def other_fixture():
    return fake.pystr()


@pytest.fixture(name="invalid_hash")
def invalid_hash_fixture():
    return fake.sha256()


@pytest.mark.unit
def test_dummy_verify(secret):
    assert not hash_service.dummy_verify(secret)


@pytest.mark.unit
class TestVerify:
    def test_valid_hash(self, secret):
        result = hash_service.hash_(secret)
        assert hash_service.verify(secret, result)

    def test_invalid_hash(self, secret, other):
        other_hash = hash_service.hash_(other)
        assert not hash_service.verify(secret, other_hash)

    def test_invalid_value(self, secret, invalid_hash):
        with pytest.raises(ValueError, match="hash could not be identified"):
            hash_service.verify(secret, invalid_hash)


@pytest.mark.unit
class TestHash:
    def test_hash_secret(self, secret):
        hash_ = hash_service.hash_(secret)
        assert secret != hash_

    def test_hash_must_be_verifiable(self, secret):
        hash_ = hash_service.hash_(secret)
        assert hash_service.verify(secret, hash_)

    def test_hash_same_secret_must_be_different(self, secret):
        assert hash_service.hash_(secret) != hash_service.hash_(secret)

    def test_different_secrets_must_be_different(self, secret, other):
        assert hash_service.hash_(secret) != hash_service.hash_(other)
