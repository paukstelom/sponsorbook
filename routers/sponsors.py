from typing import List, Optional

from fastapi import APIRouter, HTTPException, Body

from models.contact_models import (
    Contact,
    CreateContactModel,
    CreateContactForSponsorModel,
)
from models.sponsor_models import Sponsor, CreateSponsorModel, EditSponsorModel
from storage import SponsorRepositoryDep, ContactsDep, ContactRepositoryDep

router = APIRouter(prefix="/sponsors")


@router.get("", response_description="Get sponsors")
async def get_sponsors(
    sponsors: SponsorRepositoryDep, page_size: int = 100
) -> List[Sponsor]:
    return await sponsors.list(page_size)


@router.get(
    "/{sponsor_id}", response_description="Get one sponsor", response_model=Sponsor
)
async def get_sponsor(
    sponsor_id: str, sponsors: SponsorRepositoryDep
) -> Optional[Sponsor]:
    if (sponsor := await sponsors.get_by_id(sponsor_id)) is None:
        raise HTTPException(status_code=404, detail="Sponsor not found!")

    return sponsor


@router.delete("/{sponsor_id}", response_description="Delete sponsor")
async def delete_sponsor(sponsors: SponsorRepositoryDep, sponsor_id: str) -> None:
    if (sponsor := await sponsors.get_by_id(sponsor_id)) is None:
        raise HTTPException(status_code=404, detail="Sponsor not found!")

    sponsor.archive()

    await sponsors.save(sponsor)


@router.post("", response_description="Create sponsor", response_model="")
async def create_sponsor(
    sponsors: SponsorRepositoryDep,
    contacts: ContactRepositoryDep,
    data: CreateSponsorModel,
) -> str:
    sponsor = Sponsor(
        name=data.name,
        rating=data.rating,
        company_number=data.company_number,
        website=data.website,
        description=data.description,
        categories=data.categories,
    )

    await sponsors.insert(sponsor)

    for contact in data.contacts:
        contact = Contact(
            name=contact.name,
            sponsor_id=sponsor.id,
            phone=contact.phone,
            email=contact.email,
            details=contact.details,
        )
        await contacts.insert(contact)

    return str(sponsor.id)


@router.put("/{sponsor_id}", response_description="Edit sponsor")
async def update_sponsor(
    sponsors: SponsorRepositoryDep, sponsor_id: str, changes: EditSponsorModel
) -> None:
    if (sponsor := await sponsors.get_by_id(sponsor_id)) is None:
        raise HTTPException(status_code=404, detail="Sponsor not found!")

    if changes.description is not None:
        sponsor.description = changes.description

    if changes.company_number is not None:
        sponsor.company_number = changes.company_number

    if changes.name is not None:
        sponsor.name = changes.name

    if changes.categories is not None:
        sponsor.category = changes.categories

    if changes.status is not None:
        sponsor.status = changes.status

    if changes.website is not None:
        sponsor.website = changes.website

    await sponsors.save(sponsor)


@router.get("/{sponsor_id}/contacts", response_description="Get contacts for sponsor")
async def get_contacts_for_sponsor(
    sponsors: SponsorRepositoryDep, contacts: ContactRepositoryDep, sponsor_id: str
) -> List[Contact]:
    if (sponsor := await sponsors.get_by_id(sponsor_id)) is None:
        raise HTTPException(status_code=404, detail="Sponsor not found!")

    return await contacts.list_by_sponsor_id(sponsor.id)


@router.post("/{sponsor_id}/contacts", response_description="Create contact")
async def add_contact(
    sponsors: SponsorRepositoryDep,
    contacts: ContactRepositoryDep,
    sponsor_id: str,
    body: CreateContactForSponsorModel = Body(),
) -> None:
    if (sponsor := await sponsors.get_by_id(sponsor_id)) is None:
        raise HTTPException(status_code=403, detail="Sponsor not found!")

    contact = Contact(
        name=body.name,
        phone=body.phone,
        email=body.email,
        details=body.details,
        sponsor_id=sponsor.id,
    )

    await contacts.insert(contact)
