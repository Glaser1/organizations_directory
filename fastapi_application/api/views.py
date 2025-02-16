from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, status, Path, HTTPException, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from models import Organization, Activity, Building, organization_activity
from db_helper import db_helper
from api.schemas import OrganizationSchema, BuildingSchema


router = APIRouter(prefix=settings.api_prefix, tags=["Directory"])


@router.get(
    "/building/{bulding_id}/organizations", response_model=list[OrganizationSchema], status_code=status.HTTP_200_OK
)
async def get_organizations_by_building(
    bulding_id: Annotated[int, Path], session: AsyncSession = Depends(db_helper.get_db)
) -> list[Organization]:
    stmt = select(Organization).join(Building).where(Building.id == bulding_id)
    result = await session.scalars(stmt)
    return list(result.all())


@router.get(
    "/activities/organizations/{activity_id}/", response_model=list[OrganizationSchema], status_code=status.HTTP_200_OK
)
async def get_organizations_by_activity(
    activity_id: Annotated[int, Path], session: AsyncSession = Depends(db_helper.get_db)
) -> list[Organization]:
    stmt = select(Organization).join(organization_activity).join(Activity).where(Activity.id == activity_id)
    result = await session.scalars(stmt)
    return list(result.all())


@router.get(
    "/organizations/{organization_title}", response_model=list[OrganizationSchema], status_code=status.HTTP_200_OK
)
async def search_organizations_by_title(
    organization_title: str, session: AsyncSession = Depends(db_helper.get_db)
) -> list[Organization]:
    stmt = select(Organization).filter(Organization.title.ilike(f"%{organization_title}%"))
    result = await session.scalars(stmt)
    return list(result.all())


@router.get("/organizations/{organization_id}", response_model=OrganizationSchema, status_code=status.HTTP_200_OK)
async def get_organization_by_id(
    organization_id: Annotated[int, Path], session: AsyncSession = Depends(db_helper.get_db)
):
    organization = await session.get(Organization, organization_id)
    if organization:
        return organization
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Organization {organization_id} not found!")


@router.get("/buildings", response_model=list[BuildingSchema], status_code=status.HTTP_200_OK)
async def get_buildings(session: AsyncSession = Depends(db_helper.get_db)):
    stmt = select(Building).order_by(Building.id)
    result = await session.scalars(stmt)
    return result.all()


@router.get("/activities/{activity_title}/organizations", status_code=status.HTTP_200_OK)
async def get_organizations_by_activity_title(
    activity_title: Annotated[str, Path], session: AsyncSession = Depends(db_helper.get_db)
):
    parent_activity = select(Activity.title).where(Activity.title == activity_title)

    recursive_query = select(Activity.id).join(Activity, Activity.id == Activity.parent_id)

    activity_cte = parent_activity.union_all(recursive_query).cte(recursive=True)

    stmt = select(activity_cte.c.id)
    
    result = await session.execute(stmt)
    return [row[0] for row in result.all()]
