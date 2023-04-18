from typing import Tuple

from bson import ObjectId
from bson.errors import InvalidId
from pymongo.collection import Collection


def delete_ticket(tickets: Collection, archived_tickets: Collection, ticket_id: str) -> Tuple[str | dict, int]:
    try:
        mongo_id = ObjectId(ticket_id)
    except InvalidId:
        return "Id is not well-formed", 400

    ticket = tickets.find_one({'_id': mongo_id})
    if ticket is None:
        return 'Ticket not found', 400

    tickets.delete_one({'_id': mongo_id})
    archived_tickets.insert_one(ticket)
    return 'Ticket deleted', 200
