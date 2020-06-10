from pydantic import BaseModel, EmailStr, Field


class Credentials(BaseModel):
    class Config:
        allow_mutation = False

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


class User(BaseModel):
    class Config:
        allow_mutation = False

    id: int  # noqa: A003
    email: EmailStr
    password_hash: str


class UserRegistry(BaseModel):
    class Config:
        allow_mutation = False

    id: int  # noqa: A003
    email: EmailStr
