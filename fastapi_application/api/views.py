import math
from typing import Annotated

from fastapi import APIRouter, Depends, status, Path, HTTPException, HTTPException, Query
from sqlalchemy import select
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
    "/activities/organizations/{activity_id}", response_model=list[OrganizationSchema], status_code=status.HTTP_200_OK
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


@router.get("/organizations_by_id/{organization_id}", response_model=OrganizationSchema, status_code=status.HTTP_200_OK)
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

    topq = select(Activity.id).where(Activity.title == activity_title).cte(recursive=True)
    bottomq = select(Activity.id).join(topq, Activity.parent_id == topq.c.id)
    activities_tree = topq.union_all(bottomq)
    query = (
        select(Organization)
        .distinct()
        .join(organization_activity, Organization.id == organization_activity.c.organization_id)
        .where(organization_activity.c.activity_id.in_(select(activities_tree.c.id)))
    )
    result = await session.execute(query)
    return result.scalars().all()


def get_bbox(center_lat: float, center_lon: float, delta_km: float) -> tuple[float, float, float, float]:
    delta_lat = delta_km / 111.32
    delta_lon = delta_km / (111.32 * math.cos(math.radians(center_lat)))
    min_lat, max_lat = center_lat - delta_lat, center_lat + delta_lat
    min_lon, max_lon = center_lon - delta_lon, center_lon + delta_lon
    return min_lat, max_lat, min_lon, max_lon


@router.get("/organizations_by_area")
async def get_organizations_by_area(
    center_lat: Annotated[float, Query()],
    center_lon: Annotated[float, Query()],
    delta_km: Annotated[int, Query()],
    session: AsyncSession = Depends(db_helper.get_db),
):

    min_lat, max_lat, min_lon, max_lon = get_bbox(center_lat, center_lon, delta_km)

    stmt = (
        select(Organization)
        .join(Building)
        .where(Building.longitude.between(min_lon, max_lon))
        .where(Building.latitude.between(min_lat, max_lat))
    )

    result = await session.scalars(stmt)
    return result.all()

@router.get("/buildings_by_area")
async def get_buildings_by_area(
    center_lat: Annotated[float, Query()],
    center_lon: Annotated[float, Query()],
    delta_km: Annotated[int, Query()],
    session: AsyncSession = Depends(db_helper.get_db),
):

    min_lat, max_lat, min_lon, max_lon = get_bbox(center_lat, center_lon, delta_km)

    stmt = (
        select(Building)
        .where(Building.longitude.between(min_lon, max_lon))
        .where(Building.latitude.between(min_lat, max_lat))
    )

    result = await session.scalars(stmt)
    return result.all()
