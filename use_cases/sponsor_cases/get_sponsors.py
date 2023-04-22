from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorCollection

from models.sponsor_models import Sponsor


async def get_sponsors(sponsors: AsyncIOMotorCollection, page_size: int = 100) -> AsyncGenerator[Sponsor, None]:
    for sponsors in await sponsors.find().to_list(page_size):
        yield Sponsor.parse_obj(sponsors)
