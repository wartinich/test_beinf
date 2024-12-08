from pydantic import BaseModel


class SignInRequest(BaseModel):
    username: str
    password: str


class SignInResponse(BaseModel):
    access_token: str
    id_token: str
    refresh_token: str


class SignOutRequest(BaseModel):
    access_token: str
