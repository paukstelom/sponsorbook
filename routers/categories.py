from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder

from storage import DatabaseDep
from models.category_models import Category, CreateCategoryModel

router = APIRouter(prefix="/categories")


@router.get("", response_description="Get categories")
async def get_all_categories(
    database: DatabaseDep, page_size: int = 100
) -> List[Category]:
    return (
        await database["categories"]
        .find({"is_archived": False})
        .to_list(length=page_size)
    )


@router.get(
    "/{category_id}", response_description="Get one category", response_model=Category
)
async def get_one_category(
    category_id: str, database: DatabaseDep
) -> Optional[Category]:
    category = await database.categories.find_one(
        {"_id": category_id, "is_archived": False}
    )

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found!")

    return category


@router.delete("/{category_id}", response_description="Delete category")
async def delete_category(database: DatabaseDep, category_id: str) -> None:
    res = await database.categories.update_one(
        {"_id": category_id}, {"$set": {"is_archived": True}}
    )
    if res.matched_count != 1:
        raise HTTPException(status_code=404, detail="Category not found!")


@router.post("", response_description="Create category", response_model="")
async def create_category(
    database: DatabaseDep, data: CreateCategoryModel = Body()
) -> Category:
    category = Category(name=data.name, info=data.info)

    await database.categories.insert_one(jsonable_encoder(category))
    return category
