from fastapi import HTTPException

from auth.services import cognito_client


def verify_token(access_token: str):
    try:
        cognito_client.get_user(AccessToken=access_token)
    except cognito_client.exceptions.NotAuthorizedException:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
