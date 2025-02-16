import asyncio
import json

from sqlalchemy import select, delete

from models import Building, Activity, PhoneNumber, Organization, organization_activity
from db_helper import db_helper

with open("test_data.json", "r") as f:
    data = json.load(f)


async def seed_test_data():
    async with db_helper.session_factory() as session:
        try:
            await session.execute(delete(organization_activity))
            await session.execute(delete(PhoneNumber))
            await session.execute(delete(Organization))
            await session.execute(delete(Activity))
            await session.execute(delete(Building))
            await session.commit()

            for building in data["buildings"]:
                session.add(Building(**building))

            for activity in data["activities"]:
                session.add(Activity(**activity))

            for org in data["organizations"]:
                organization = Organization(
                    id=org["id"],
                    title=org["title"],
                    building_id=org["building_id"],
                )
                stmt = select(Activity).filter(Activity.id.in_(org["activity_ids"]))
                activities = await session.scalars(stmt)
                organization.activities = activities.all()
                session.add(organization)
                await session.commit()

            for phone in data["phone_numbers"]:
                session.add(PhoneNumber(**phone))

            await session.commit()
            print("Данные успешно добавлены")
        except Exception as e:
            await session.rollback()
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    asyncio.run(seed_test_data())
