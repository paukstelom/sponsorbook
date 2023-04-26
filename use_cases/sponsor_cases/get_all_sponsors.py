from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorDatabase

from models.sponsor_models import Sponsor


async def get_sponsors(database: AsyncIOMotorDatabase, page_size: int = 100) -> AsyncGenerator[Sponsor, None]:
    for sponsor in await database.sponsors.find().to_list(page_size):
        yield Sponsor.parse_obj(sponsor)
