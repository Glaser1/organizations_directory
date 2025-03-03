from typing import Optional

from geoalchemy2.shape import to_shape
from pydantic import BaseModel, constr, PositiveInt, field_validator
from pydantic_extra_types.coordinate import Latitude, Longitude


class BuildingSchema(BaseModel):
    id: int
    address: str
    geo_location: str

    @field_validator("geo_location", mode="before")
    @classmethod
    def turn_geo_location_into_wkt(cls, value):
        return to_shape(value).wkt


class OrganizationSchema(BaseModel):
    title: str
    building_id: int


class NearbyObjectsByCoordsSchema(BaseModel):
    km_within: PositiveInt
    latitude: Latitude
    longitude: Longitude
