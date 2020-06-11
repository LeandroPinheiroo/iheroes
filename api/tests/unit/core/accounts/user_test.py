from functools import partial

import pytest
from hypothesis import given
from hypothesis import strategies as st
from pydantic import ValidationError

import tests.strategies as tst
from iheroes_api.core.accounts.user import Credentials, User, UserRegistry
from tests.utils.asserts import assert_validation_error


# Credentials
@pytest.mark.unit
@pytest.mark.hypothesis
class TestCredentials:
    class TestModel:
        valid_st = st.fixed_dictionaries(
            {"email": tst.emails(), "password": tst.passwords()}
        )
        invalid_st = st.fixed_dictionaries(
            {
                "email": st.text(),
                "password": st.one_of(st.text(max_size=7), st.text(min_size=129)),
            }
        )

        @given(valid_st)
        def test_validation(self, data):
            assert Credentials(**data)

        @given(invalid_st)
        def test_invalidation(self, data):
            with pytest.raises(ValidationError):
                Credentials(**data)

        @given(valid_st)
        def test_immutability(self, data):
            entity = Credentials(**data)
            for key in entity.dict().keys():
                with pytest.raises(TypeError):
                    setattr(entity, key, "some value")

    class TestEmail:
        assert_validation_error = partial(assert_validation_error, 1, "email")

        @given(
            st.fixed_dictionaries(
                {"email": st.text(), "password": tst.passwords().filter(str.isalnum)}
            )
        )
        def test_must_be_email(self, data):
            with pytest.raises(ValidationError) as excinfo:
                Credentials(**data)

            self.assert_validation_error("value_error.email", excinfo)

        @given(st.fixed_dictionaries({"password": tst.passwords()}))
        def test_is_required(self, data):
            with pytest.raises(ValidationError) as excinfo:
                Credentials(**data)

            self.assert_validation_error("value_error.missing", excinfo)

    class TestPassword:
        assert_validation_error = partial(assert_validation_error, 1, "password")

        @given(st.fixed_dictionaries({"email": tst.emails()}))
        def test_is_required(self, data):
            with pytest.raises(ValidationError) as excinfo:
                Credentials(**data)

            self.assert_validation_error("value_error.missing", excinfo)

        @given(
            st.fixed_dictionaries(
                {"email": tst.emails(), "password": st.text(max_size=7)}
            )
        )
        def test_min_length_gte_8(self, data):
            with pytest.raises(ValidationError) as excinfo:
                Credentials(**data)

            self.assert_validation_error("value_error.any_str.min_length", excinfo)

        @given(
            st.fixed_dictionaries(
                {"email": tst.emails(), "password": st.text(min_size=129, max_size=256)}
            )
        )
        def test_max_length_lte_128(self, data):
            with pytest.raises(ValidationError) as excinfo:
                Credentials(**data)

            self.assert_validation_error("value_error.any_str.max_length", excinfo)


# User
@pytest.mark.unit
@pytest.mark.hypothesis
class TestUser:
    class TestModel:
        valid_st = st.fixed_dictionaries(
            {
                "id": tst.ids(),
                "email": tst.emails(),
                "password_hash": tst.password_hashes(),
            }
        )
        invalid_st = st.fixed_dictionaries(
            {
                "id": st.text().filter(lambda i: not i.isnumeric()),
                "email": st.text(),
                "password_hash": st.one_of(st.iterables(st.text())),
            }
        )

        @given(valid_st)
        def test_validation(self, data):
            assert User(**data)

        @given(invalid_st)
        def test_invalidation(self, invalid_data):
            with pytest.raises(ValidationError):
                assert User(**invalid_data)

        @given(valid_st)
        def test_immutability(self, data):
            entity = User(**data)
            for key in entity.dict().keys():
                with pytest.raises(TypeError):
                    setattr(entity, key, "some value")

    class TestId:
        assert_validation_error = partial(assert_validation_error, 1, "id")

        @given(
            st.fixed_dictionaries(
                {"email": tst.emails(), "password_hash": tst.password_hashes()}
            )
        )
        def test_is_required(self, data):
            with pytest.raises(ValidationError) as excinfo:
                User(**data)

            self.assert_validation_error("value_error.missing", excinfo)

    class TestEmail:
        assert_validation_error = partial(assert_validation_error, 1, "email")

        @given(
            st.fixed_dictionaries(
                {
                    "id": tst.ids(),
                    "email": st.text(),
                    "password_hash": tst.password_hashes(),
                }
            )
        )
        def test_must_be_email(self, data):
            with pytest.raises(ValidationError) as excinfo:
                User(**data)

            self.assert_validation_error("value_error.email", excinfo)

        @given(
            st.fixed_dictionaries(
                {"id": tst.ids(), "password_hash": tst.password_hashes()}
            )
        )
        def test_is_required(self, data):
            with pytest.raises(ValidationError) as excinfo:
                User(**data)

            self.assert_validation_error("value_error.missing", excinfo)

    class TestPasswordHash:
        assert_validation_error = partial(assert_validation_error, 1, "password_hash")

        @given(st.fixed_dictionaries({"id": tst.ids(), "email": tst.emails()}))
        def test_is_required(self, data):
            with pytest.raises(ValidationError) as excinfo:
                User(**data)

            self.assert_validation_error("value_error.missing", excinfo)


@pytest.mark.unit
@pytest.mark.hypothesis
class TestUserRegistry:
    class TestModel:
        valid_st = st.fixed_dictionaries({"id": tst.ids(), "email": tst.emails()})
        invalid_st = st.fixed_dictionaries(
            {"id": st.text().filter(lambda i: not i.isnumeric()), "email": st.text()}
        )

        @given(valid_st)
        def test_validation(self, data):
            assert UserRegistry(**data)

        @given(invalid_st)
        def test_invalidation(self, invalid_data):
            with pytest.raises(ValidationError):
                assert UserRegistry(**invalid_data)

        @given(valid_st)
        def test_immutability(self, data):
            entity = UserRegistry(**data)
            for key in entity.dict().keys():
                with pytest.raises(TypeError):
                    setattr(entity, key, "some value")

    class TestId:
        assert_validation_error = partial(assert_validation_error, 1, "id")

        @given(
            st.fixed_dictionaries(
                {"email": tst.emails(), "password_hash": tst.password_hashes()}
            )
        )
        def test_is_required(self, data):
            with pytest.raises(ValidationError) as excinfo:
                UserRegistry(**data)

            self.assert_validation_error("value_error.missing", excinfo)

    class TestEmail:
        assert_validation_error = partial(assert_validation_error, 1, "email")

        @given(
            st.fixed_dictionaries(
                {
                    "id": tst.ids(),
                    "email": st.text(),
                    "password_hash": tst.password_hashes(),
                }
            )
        )
        def test_must_be_email(self, data):
            with pytest.raises(ValidationError) as excinfo:
                UserRegistry(**data)

            self.assert_validation_error("value_error.email", excinfo)

        @given(
            st.fixed_dictionaries(
                {"id": tst.ids(), "password_hash": tst.password_hashes()}
            )
        )
        def test_is_required(self, data):
            with pytest.raises(ValidationError) as excinfo:
                UserRegistry(**data)

            self.assert_validation_error("value_error.missing", excinfo)
