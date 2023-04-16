from dataclasses import dataclass


@dataclass
class Event:
    id: str
    description: str | None
    contact_method: str
    contact_details: str
    datetime: str
    creator_id: str


@dataclass
class Ticket:
    id: str
    title: str
    datetime: str
    description: str | None
    active: bool
    creator_id: str
    events: list[Event]


@dataclass
class User:
    id: str
    access: str


@dataclass
class Sponsor:
    name: str
    description: str
    tickets: list[Ticket]


@dataclass
class SubOrganization:
    name: str
    sponsors: list[Sponsor]
    users: list[User]


@dataclass
class Organization:
    id: str
    name: str
    # details: dict | None
    sub_organizations: list[SubOrganization]
