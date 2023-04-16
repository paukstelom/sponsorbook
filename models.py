from dataclasses import dataclass


@dataclass
class Ticket:
    id: str
    title: str
    description: str


@dataclass
class User:
    pass


@dataclass
class Sponsor:
    name: str
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
    sub_organizations: list[SubOrganization]
