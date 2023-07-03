from fastapi import APIRouter, HTTPException, Body

from models.contact_models import CreateContactModel, Contact
from storage import SponsorRepositoryDep, ContactRepositoryDep

router = APIRouter(prefix="/contacts")


@router.post("", response_description="Create contact")
async def add_contact(
    sponsors: SponsorRepositoryDep,
    contacts: ContactRepositoryDep,
    body: CreateContactModel = Body(),
) -> None:
    if (sponsor := await sponsors.get_by_id(body.sponsor_id)) is None:
        raise HTTPException(status_code=403, detail="Sponsor not found!")

    contact = Contact(
        name=body.name,
        phone=body.phone,
        email=body.email,
        details=body.details,
        sponsor_id=sponsor.id,
    )

    await contacts.insert(contact)


@router.delete("/{contact_id}", response_description="Delete contact")
async def delete_contact(contacts: ContactRepositoryDep, contact_id: str) -> None:
    if (contact := await contacts.get_by_id(contact_id)) is None:
        raise HTTPException(status_code=404, detail="Contact not found!")

    contact.archive()

    await contacts.save(contact)
