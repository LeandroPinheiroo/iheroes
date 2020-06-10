import hypothesis.strategies as st
from email_validator import EmailNotValidError, validate_email
from toolz.functoolz import excepts

from iheroes_api.core.accounts import hash_service


# Hypothesis generates emails as specified by
# [RFC 5322#section-3.4.1](https://tools.ietf.org/html/rfc5322.html#section-3.4.1)
#
# But Pydantic's EmailStr type uses email_validator to validate emails, which
# doesn't follow the RFC rules. This strategy generates emails that
# pass the email_validator validation so it is not necessary to write
# separate validator from Pydantic.
def emails():
    return st.emails().filter(
        excepts(
            EmailNotValidError,
            lambda e: validate_email(e, check_deliverability=False),
            lambda _: False,
        )
    )


def passwords():
    return st.text(min_size=8, max_size=128)


def password_hashes():
    return passwords().map(hash_service.hash_)
