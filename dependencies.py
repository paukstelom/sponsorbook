from typing import Annotated

from fastapi import Cookie, HTTPException


def cookie_extractor(
        session: Annotated[str | None, Cookie()] = None,
):
    if session is None:
        raise HTTPException(status_code=403, detail="Session missing")

    return session
