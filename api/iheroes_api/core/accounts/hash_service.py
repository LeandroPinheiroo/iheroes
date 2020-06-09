from passlib.context import CryptContext

_context = CryptContext(schemes=["argon2"], deprecated="auto")

dummy_verify = _context.dummy_verify
verify = _context.verify


def hash_(secret: str) -> str:
    return str(_context.hash(secret))
