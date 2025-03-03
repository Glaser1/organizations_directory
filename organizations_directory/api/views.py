from typing import Annotated, Optional, Type

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2.functions import ST_AsText, ST_DWithin, ST_GeogFromText

from api.schemas import BuildingSchema, NearbyObjectsByCoordsSchema, OrganizationSchema
from config import settings
from db_helper import db_helper
from models import Activity, Building, Organization, organization_activity

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


async def get_objects_by_area(
    model: Type,
    coords_schema: NearbyObjectsByCoordsSchema,
    session: AsyncSession = Depends(db_helper.get_db),
    join_model: Optional[Type] = None,
):
    latitude, longitude, km_within = coords_schema.latitude, coords_schema.longitude, coords_schema.km_within
    target_geography = ST_GeogFromText(f"POINT({longitude} {latitude})", srid=4326)

    stmt = select(model)

    if join_model:
        stmt = stmt.join(join_model).where(ST_DWithin(join_model.geo_location, target_geography, 1000 * km_within))
    else:
        stmt = stmt.where(ST_DWithin(model.geo_location, target_geography, 1000 * km_within))

    result = await session.scalars(stmt)
    return result.all()


@router.post("/buildings_by_area", response_model=list[BuildingSchema])
async def get_buildings_by_area(
    coords_schema: NearbyObjectsByCoordsSchema, session: AsyncSession = Depends(db_helper.get_db)
):
    return await get_objects_by_area(Building, coords_schema, session)


@router.post("/ogranizations_by_area", response_model=list[OrganizationSchema])
async def get_organizations_by_area(
    coords_schema: NearbyObjectsByCoordsSchema, session: AsyncSession = Depends(db_helper.get_db)
):
    return await get_objects_by_area(Organization, coords_schema, session, Building)
