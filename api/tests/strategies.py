import hypothesis.strategies as st
from email_validator import EmailNotValidError, validate_email
from toolz.functoolz import excepts

from iheroes_api.core.accounts import hash_service
from iheroes_api.core.accounts.user import Credentials, User, UserRegistry

# Type strategies


def emails():
    """Generate Pydantic's EmailStr compatible email.

    Hypothesis generates emails as specified by
    [RFC 5322#section-3.4.1](https://tools.ietf.org/html/rfc5322.html#section-3.4.1)

    But Pydantic's EmailStr type uses email_validator to validate emails, which
    doesn't follow the RFC rules. This strategy generates emails that
    pass the email_validator validation so it is not necessary to write
    a separate validator from Pydantic's default.
    """
    return st.emails().filter(
        excepts(
            EmailNotValidError,
            lambda e: validate_email(e, check_deliverability=False),
            lambda _: False,
        )
    )


def ids():
    return st.integers(min_value=0)


def passwords(min_size=8, max_size=128):
    return st.text(min_size=min_size, max_size=max_size)


def password_hashes(min_size=8, max_size=128, hasher=hash):
    return passwords(min_size, max_size).map(hasher).map(str)


# Entity strategies


def credentials():
    return st.builds(Credentials, email=emails(), password=passwords())


def users():
    return st.builds(
        User,
        id=ids(),
        email=emails(),
        password_hash=password_hashes(hasher=hash_service.hash_),
    )


def users_registry():
    return st.builds(UserRegistry, id=ids(), email=emails())
