from typing import Tuple

from bson import ObjectId
from pymongo.collection import Collection

from database_utils.gen_mongo_id import gen_mongo_id
from models.ticket import Ticket


def create_ticket(tickets: Collection, input: dict) -> Tuple[str | dict, int]:
    try:
        ticket = Ticket(id=str(gen_mongo_id()), title=input['title'],
                        description=input['description'])
    except KeyError:
        return 'Missing fields', 400

    tickets.insert_one({'_id': ObjectId(ticket.id),
                        'title': ticket.title,
                        'description:': ticket.description})
    return ticket.__dict__, 201
