import motor.motor_asyncio as ma

from infrastructure import CollectionRepository
from infrastructure.CollectionRepository import CollectionRepository


async def get_db_session() -> ma.AsyncIOMotorClientSession:
    client = ma.AsyncIOMotorClient(replicaset="rs0")

    async with await client.start_session() as session:
        async with session.start_transaction():
            yield session
