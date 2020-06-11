import pytest
from hypothesis import given
from hypothesis import strategies as st

import tests.strategies as tst
from iheroes_api.core.accounts.exceptions import EmailNotUniqueError, UserNotFoundError


@pytest.mark.unit
@given(tst.emails(), st.text())
def test_email_not_unique_error(email, msg):
    error = EmailNotUniqueError(email, msg)
    assert error.as_dict() == {"msg": msg, "email": email}

    with pytest.raises(EmailNotUniqueError):
        raise error


@pytest.mark.unit
@given(st.integers(), st.text())
def test_user_not_found_error(id_, msg):
    id_ = 1
    msg = "some message"

    error = UserNotFoundError(id_, msg)
    assert error.as_dict() == {"msg": msg, "user_id": id_}

    with pytest.raises(UserNotFoundError):
        raise error
