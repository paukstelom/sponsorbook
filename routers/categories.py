from typing import List, Optional

from fastapi import APIRouter, Body, HTTPException

from models.category_models import Category, CreateCategoryModel
from dependencies.infrastructure import CategoryRepositoryDep

router = APIRouter(prefix="/categories")


@router.get("", response_description="Get categories")
async def get_all_categories(
    categories: CategoryRepositoryDep, page_size: int = 100
) -> List[Category]:
    return await categories.list(page_size)


@router.get("/{category_id}", response_description="Get one category")
async def get_one_category(
    category_id: str, categories: CategoryRepositoryDep
) -> Optional[Category]:
    if (category := await categories.get_by_id(category_id)) is None:
        raise HTTPException(status_code=404, detail="Category not found!")

    return category


@router.delete("/{category_id}", response_description="Delete category")
async def delete_category(categories: CategoryRepositoryDep, category_id: str) -> None:
    if (category := await categories.get_by_id(category_id)) is None:
        raise HTTPException(status_code=404, detail="Category not found!")

    category.archive()

    await categories.save(category)


@router.post("", response_description="Create category")
async def create_category(
    categories: CategoryRepositoryDep, data: CreateCategoryModel = Body()
) -> Category:
    category = Category(name=data.name, info=data.info)
    await categories.insert(category)
    return category
