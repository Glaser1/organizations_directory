from typing import Optional

from pydantic import BaseModel, constr


class BuildingSchema(BaseModel):
    id: int
    address: str
    latitude: float
    longitude: float


class ActivitySchema(BaseModel):
    name: str
    parent_id: Optional[int]
    organizations: list["OrganizationSchema"]
    children: list["ActivitySchema"]


class PhoneNumberSchema(BaseModel):
    phone: str
    title: str
    organization_id: int


class OrganizationSchema(BaseModel):
    title: str 
    building_id: int
