from typing import Tuple

from pymongo.collection import Collection


def get_tickets(tickets: Collection) -> Tuple[list, int]:
    return list(tickets.find({}, {"_id": False})), 200
