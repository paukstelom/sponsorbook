from pydantic import Field

from models.base import EntityModel, BaseModelConfig, BaseCreationModel


class Category(EntityModel):
    name: str = Field()
    info: str = Field()

    class Config(BaseModelConfig):
        schema_extra = {
            "example": {
                "_id": "123123123",
                "title": "Jane Doe",
                "description": "Bruh",
            }
        }


class CreateCategoryModel(BaseCreationModel):
    name: str = Field()
    info: str = Field()
