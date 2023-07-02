from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder

from models.category_models import Category, CreateCategoryModel
from storage import CategoriesDep

router = APIRouter(prefix="/categories")


@router.get("", response_description="Get categories")
async def get_all_categories(
    categories: CategoriesDep, page_size: int = 100
) -> List[Category]:
    return await categories.find({"is_archived": False}).to_list(length=page_size)


@router.get(
    "/{category_id}", response_description="Get one category", response_model=Category
)
async def get_one_category(
    category_id: str, categories: CategoriesDep
) -> Optional[Category]:
    category = await categories.find_one({"_id": category_id, "is_archived": False})

    if category is None:
        raise HTTPException(status_code=404, detail="Category not found!")

    return category


@router.delete("/{category_id}", response_description="Delete category")
async def delete_category(categories: CategoriesDep, category_id: str) -> None:
    res = await categories.update_one(
        {"_id": category_id}, {"$set": {"is_archived": True}}
    )
    if res.matched_count != 1:
        raise HTTPException(status_code=404, detail="Category not found!")


@router.post("", response_description="Create category", response_model="")
async def create_category(
    categories: CategoriesDep, data: CreateCategoryModel = Body()
) -> Category:
    category = Category(name=data.name, info=data.info)

    await categories.insert_one(jsonable_encoder(category))
    return category
