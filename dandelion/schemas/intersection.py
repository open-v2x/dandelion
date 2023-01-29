# Copyright 2022 99Cloud, Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


# Shared properties
class IntersectionBase(BaseModel):
    code: str = Field(..., alias="code", description="Intersection code")
    name: str = Field(..., alias="name", description="Intersection name")
    lat: str = Field(..., alias="lat", description="Intersection latitude")
    lng: str = Field(..., alias="lng", description="Intersection longitude")
    area_code: str = Field(..., alias="areaCode", description="Area Code")


# Properties to receive via API on creation
class IntersectionCreate(IntersectionBase):
    """"""


# Properties to receive via API on update
class IntersectionUpdate(BaseModel):
    """"""

    name: Optional[str] = Field(None, alias="name", description="Intersection name")
    lat: Optional[str] = Field(None, alias="lat", description="Intersection latitude")
    lng: Optional[str] = Field(None, alias="lng", description="Intersection longitude")
    area_code: Optional[str] = Field(None, alias="areaCode", description="Area Code")


class IntersectionInDBBase(IntersectionBase):
    id: int = Field(..., alias="id", description="Intersection ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class Intersection(IntersectionInDBBase):
    """"""

    country_code: str = Field(..., alias="countryCode", description="Country Code")
    country_name: str = Field(..., alias="countryName", description="Country Name")
    province_code: str = Field(..., alias="provinceCode", description="Province Code")
    province_name: str = Field(..., alias="provinceName", description="Province Name")
    city_code: str = Field(..., alias="cityCode", description="City Code")
    city_name: str = Field(..., alias="cityName", description="City Name")
    area_code: str = Field(..., alias="areaCode", description="Area Code")
    area_name: str = Field(..., alias="areaName", description="Area Name")


class Intersections(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[Intersection] = Field(..., alias="data", description="Data")
