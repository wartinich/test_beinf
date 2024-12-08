from fastapi import APIRouter

from auth.schemas import SignInResponse, SignInRequest, SignOutRequest
from auth.services import sign_in, sign_out

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login/", response_model=SignInResponse)
def login(request: SignInRequest):
    return sign_in(request)


@router.post("/logout/")
def logout(request: SignOutRequest):
    return sign_out(request)
