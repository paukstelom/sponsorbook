from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class Ticket:
    id: str
    title: str
    description: str


class TicketModel(BaseModel):
    id: str
    title: str
    description: str

