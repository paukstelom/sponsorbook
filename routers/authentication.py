from argon2.exceptions import VerifyMismatchError
from fastapi import Body, APIRouter, HTTPException
from starlette.responses import Response

from dependencies import (
    GetPasswordHasherDep,
    RequireSession,
    RequireUser,
    EncodeSessionDep,
    VerifyPasswordDep,
    HashPasswordDep,
)
from models.authentication_models import Credentials
from models.session import SessionWithUser
from storage.UserCollectionRepository import UserRepositoryDep

router = APIRouter(prefix="/auth")


@router.post("/login", response_description="Login")
async def login_endpoint(
    users: UserRepositoryDep,
    encode: EncodeSessionDep,
    verify: VerifyPasswordDep,
    credentials: Credentials = Body(...),
):
    if (user := await users.get_by_email(credentials.email)) is None:
        raise HTTPException(
            status_code=401, detail="User with that email doesn't exist"
        )

    if not verify(credentials.password, user):
        raise HTTPException(status_code=401, detail="Password incorrect")

    token = encode(user)
    response = Response()
    response.set_cookie(key="session", value=token, max_age=64 * 64)
    return response


@router.get("/session")
async def get_session_endpoint(session: RequireSession, user: RequireUser):
    return SessionWithUser(session=session, user=user)
