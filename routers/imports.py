from io import BytesIO
from typing import Annotated

import pandas as pd
import numpy as np
from fastapi import APIRouter, File, UploadFile, HTTPException

from models.category_models import Category
from models.contact_models import Contact
from models.py_object_id import PyObjectId
from models.sponsor_models import Sponsor, Rating
from storage.CategoryCollectionRepository import CategoryRepositoryDep
from storage.ContactCollectionRepository import ContactRepositoryDep
from storage.SponsorCollectionRepository import SponsorRepositoryDep

router = APIRouter(prefix="/imports")


def get_or_default(value, default):
    return value if not pd.isna(value) else default


@router.post("", response_description="Create an event")
async def _import(
    sponsors: SponsorRepositoryDep,
    categories: CategoryRepositoryDep,
    contacts: ContactRepositoryDep,
    file: Annotated[UploadFile | None, File()],
):
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=403, detail="Invalid format")

    contents = file.file.read()
    data = BytesIO(contents)

    dfs = pd.read_excel(data, sheet_name=None)
    file.file.close()

    contacts_to_insert = []
    categories_inserted = {}
    for df in dfs.values():
        for row in df.iloc:
            sponsor_id = PyObjectId()
            category_name = get_or_default(row[1], "Unknown")

            if (
                category := await categories.get_by_name(category_name)
            ) is None and category_name not in categories_inserted:
                category = Category(name=category_name, info="")
                await categories.insert(category)
                categories_inserted[category_name] = category
            elif category_name in categories_inserted:
                category = categories_inserted[category_name]

            sponsor_name = get_or_default(row[0], "Unknown sponsor name")
            status = get_or_default(row[2], "Unknown")
            phone = get_or_default(row[4], "Unknown phone")
            email = get_or_default(row[3], "Unknown email")
            contact_name = get_or_default(row[5], "Unknown name")
            comment = get_or_default(row[7], "")
            website = get_or_default(row[6], "Unknown website")

            if await contacts.get_by_email(email) is None:
                contact = Contact(
                    name=contact_name,
                    phone=phone,
                    details=comment,
                    sponsor_id=sponsor_id,
                    email=email,
                )
                contacts_to_insert.append(contact)

            sponsor = Sponsor(
                id=sponsor_id,
                name=sponsor_name,
                company_number="1212121212",
                website=website,
                categories=[category.id],
                status=status,
                rating=Rating(score="2.5", info=""),
                description=comment,
            )

            await sponsors.insert(sponsor)

    for contact in contacts_to_insert:
        await contacts.insert(contact)
