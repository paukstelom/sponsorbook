from typing import List

from fastapi import APIRouter, HTTPException

from dependencies import GetPasswordHasherDep
from models.user_models import User, CreateUserModel
from storage.UserCollectionRepository import UserRepositoryDep
from storage.OrgRepositoryCollection import OrgRepositoryDep

router = APIRouter(prefix="/users")


@router.post("", response_description="Create a user")
async def create_user(
    users: UserRepositoryDep,
    orgs: OrgRepositoryDep,
    hasher: GetPasswordHasherDep,
    data: CreateUserModel,
) -> User:
    if (organization := await orgs.get_by_id(data.organization_id)) is None:
        raise HTTPException(status_code=404, detail="Organization not found!")

    hashed_password = hasher.hash(data.password)
    user = User(
        email=data.email,
        type=data.type,
        password=hashed_password,
        organization_id=organization.id,
    )

    await users.insert(user)
    return user


@router.get("/{user_id}", response_description="Get a user")
async def get_user(user_id: str, users: UserRepositoryDep) -> User:
    if (user := await users.get_by_id(user_id)) is None:
        raise HTTPException(status_code=404, detail="User not found!")

    return user


@router.get("", response_description="Get all users")
async def get_users(users: UserRepositoryDep, page_size: int = 100) -> List[User]:
    return await users.list(page_size)


@router.delete("/{user_id}", response_description="Archive a user")
async def delete_user(users: UserRepositoryDep, user_id: str) -> None:
    if (user := await users.get_by_id(user_id)) is None:
        raise HTTPException(status_code=404, detail="User not found!")

    user.archive()

    await users.save(user)
