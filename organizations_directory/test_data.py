import asyncio

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from geoalchemy2.functions import ST_Point

from organizations_directory.models import Building
from organizations_directory.db_helper import db_helper


async def create_test_buildings():
    async for session in db_helper.get_db():
        test_buildings = [
            Building(address="Building 1", geo_location=ST_Point(37.609943, 55.649648, srid=4326)),
            Building(address="Building 2", geo_location=ST_Point(37.620000, 55.650000, srid=4326)),
        ]
        session.add_all(test_buildings)
        await session.commit()
        print("Test buildings added successfully")


asyncio.run(create_test_buildings())
