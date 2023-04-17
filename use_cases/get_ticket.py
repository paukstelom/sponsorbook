from typing import Tuple
from bson import ObjectId
from bson.errors import InvalidId
from pymongo.collection import Collection


def get_ticket(id: str, tickets: Collection) -> Tuple[any, int]:
    try:
        mongo_id = ObjectId(id)
    except InvalidId:
        return "Id is not well-formed", 400

    ticket = tickets.find_one({'_id': mongo_id}, {"_id": False})

    if ticket is None:
        return "Ticket not found", 404

    return ticket, 200

