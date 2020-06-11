import pytest
from hypothesis import assume, given, settings
from hypothesis import strategies as st

import tests.strategies as tst
from iheroes_api.core.accounts import hash_service


@pytest.mark.unit
@settings(deadline=None)
@given(st.text())
def test_dummy_verify(data):
    assert not hash_service.dummy_verify(data)


@pytest.mark.unit
@pytest.mark.hypothesis
class TestVerify:
    @settings(deadline=None)
    @given(st.text())
    def test_valid_hash(self, secret):
        result = hash_service.hash_(secret)
        assert hash_service.verify(secret, result)

    @settings(deadline=None)
    @given(st.text(), st.text())
    def test_invalid_hash(self, secret, other):
        assume(secret != other)
        other_hash = hash_service.hash_(other)
        assert not hash_service.verify(secret, other_hash)

    @settings(deadline=None)
    @given(st.text(), tst.password_hashes())
    def test_invalid_value(self, secret, invalid_hash):
        with pytest.raises(ValueError, match="hash could not be identified"):
            hash_service.verify(secret, invalid_hash)


@pytest.mark.unit
@pytest.mark.hypothesis
class TestHash:
    @settings(deadline=None)
    @given(st.text())
    def test_hash_secret(self, secret):
        hash_ = hash_service.hash_(secret)
        assert secret != hash_

    @settings(deadline=None)
    @given(st.text())
    def test_hash_must_be_verifiable(self, secret):
        hash_ = hash_service.hash_(secret)
        assert hash_service.verify(secret, hash_)

    @settings(deadline=None)
    @given(st.text())
    def test_hash_same_secret_must_be_different(self, secret):
        assert hash_service.hash_(secret) != hash_service.hash_(secret)

    @settings(deadline=None)
    @given(st.text(), st.text())
    def test_different_secrets_must_be_different(self, secret, other):
        assert hash_service.hash_(secret) != hash_service.hash_(other)
