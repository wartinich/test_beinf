import os

import boto3

from fastapi import HTTPException

from auth.schemas import SignInResponse, SignOutRequest, SignInRequest
from auth.utils import calculate_secret_hash

COGNITO_USER_POOL_ID = os.environ.get("COGNITO_USER_POOL_ID")
COGNITO_APP_CLIENT_ID = os.environ.get("COGNITO_APP_CLIENT_ID")
COGNITO_APP_CLIENT_SECRET = os.environ.get("COGNITO_APP_CLIENT_SECRET")
cognito_client = boto3.client("cognito-idp", region_name="us-east-1")


def verify_token(access_token: str):
    try:
        cognito_client.get_user(AccessToken=access_token)
    except cognito_client.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def sign_in(payload: SignInRequest):
    print(COGNITO_APP_CLIENT_ID, COGNITO_APP_CLIENT_SECRET, payload.username)
    response = cognito_client.initiate_auth(
        ClientId=COGNITO_APP_CLIENT_ID,
        AuthFlow="USER_PASSWORD_AUTH",
        AuthParameters={
            "USERNAME": payload.username,
            "PASSWORD": payload.password,
            "SECRET_HASH": calculate_secret_hash(
                COGNITO_APP_CLIENT_ID, COGNITO_APP_CLIENT_SECRET, payload.username
            ),
        },
    )
    return SignInResponse(
        access_token=response["AuthenticationResult"]["AccessToken"],
        id_token=response["AuthenticationResult"]["IdToken"],
        refresh_token=response["AuthenticationResult"]["RefreshToken"],
    )


def sign_out(payload: SignOutRequest):
    try:
        cognito_client.global_sign_out(
            AccessToken=payload.access_token
        )
        return {"message": "Signed out successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
