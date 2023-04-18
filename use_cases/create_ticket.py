from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pymongo.collection import Collection
from starlette.responses import JSONResponse

from database_utils.gen_mongo_id import gen_mongo_id
from models.ticket import CreateTicketModel, Ticket


def create_ticket(tickets: Collection, data: CreateTicketModel) -> Ticket | HTTPException:
    try:
        ticket = Ticket(
            id=gen_mongo_id(),
            title=data.title,
            description=data.description)
    except KeyError:
        return HTTPException(status_code=400, detail='Missing fields')

    tickets.insert_one(jsonable_encoder(ticket))
    return ticket
