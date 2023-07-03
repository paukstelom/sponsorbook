from argon2.exceptions import VerifyMismatchError
from fastapi import Body, APIRouter, HTTPException
from starlette.responses import Response

from dependencies import (
    GetPasswordHasherDep,
    GetSessionDep,
    GetUserFromSessionDep,
    SessionEncoderDep,
)
from models.authentication_models import Credentials
from models.session import SessionWithUser
from storage import UserRepositoryDep

router = APIRouter(prefix="/auth")


@router.post("/login", response_description="Login")
async def login_endpoint(
    users: UserRepositoryDep,
    hasher: GetPasswordHasherDep,
    encoder: SessionEncoderDep,
    credentials: Credentials = Body(...),
):
    if (user := await users.get_by_email(credentials.email)) is None:
        raise HTTPException(status_code=403, detail="Bad credentials")

    try:
        hasher.verify(user.password, credentials.password)
    except VerifyMismatchError:
        raise HTTPException(status_code=403, detail="Bad credentials")

    token = encoder.encode(user)
    response = Response()
    response.set_cookie(key="session", value=token, max_age=64 * 64)
    return response


@router.get("/session")
async def get_session_endpoint(session: GetSessionDep, user: GetUserFromSessionDep):
    return SessionWithUser(session=session, user=user)
