from typing import Tuple

from bson import ObjectId
from pymongo.collection import Collection

from database_utils.gen_mongo_id import gen_mongo_id
from models.ticket import TicketModel


def create_ticket(tickets: Collection, data: dict) -> Tuple[TicketModel | str, int]:
    try:
        ticket = TicketModel(
            id=str(gen_mongo_id()),
            title=data['title'],
            description=data['description'])
    except KeyError:
        return 'Missing fields', 400

    tickets.insert_one({'_id': ObjectId(ticket.id),
                        'title': ticket.title,
                        'description:': ticket.description})
    return ticket, 201
