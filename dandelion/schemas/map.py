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

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# Shared properties
class MapBase(BaseModel):
    """"""


# Properties to receive via API on creation
class MapCreate(BaseModel):
    name: str = Field(..., alias="name", description="Map Name")
    intersection_code: str = Field(..., alias="intersectionCode", description="Intersection Code")
    desc: Optional[str] = Field("", alias="desc", description="Description")
    data: Dict[str, Any] = Field(..., alias="data", description="Data")
    bitmap_filename: str = Field(..., alias="bitmapFilename", description="Bitmap Filename")


# Properties to receive via API on update
class MapUpdate(MapBase):
    name: Optional[str] = Field(None, alias="name", description="Name")
    intersection_code: Optional[str] = Field(
        None, alias="intersectionCode", description="Intersection Code"
    )
    desc: Optional[str] = Field(None, alias="desc", description="Description")
    data: Optional[Dict[str, Any]] = Field(None, alias="data", description="Data")
    bitmap_filename: Optional[str] = Field(
        None, alias="bitmapFilename", description="Bitmap Filename"
    )


class MapInDBBase(MapBase):
    id: int = Field(..., alias="id", description="Map ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class Map(MapInDBBase):
    name: str = Field(..., alias="name", description="Map Name")
    desc: str = Field(..., alias="desc", description="Description")
    amount: int = Field(..., alias="amount", description="Count of RSUs")
    lat: float = Field(..., alias="lat", description="Latitude")
    lng: float = Field(..., alias="lng", description="Longitude")
    create_time: datetime = Field(..., alias="createTime", description="Create Time")
    country_code: str = Field(..., alias="countryCode", description="Country Code")
    country_name: str = Field(..., alias="countryName", description="Country Name")
    province_code: str = Field(..., alias="provinceCode", description="Province Code")
    province_name: str = Field(..., alias="provinceName", description="Province Name")
    city_code: str = Field(..., alias="cityCode", description="City Code")
    city_name: str = Field(..., alias="cityName", description="City Name")
    area_code: str = Field(..., alias="areaCode", description="Area Code")
    area_name: str = Field(..., alias="areaName", description="Area Name")
    intersection_code: str = Field(..., alias="intersectionCode", description="Intersection Code")
    intersection_name: str = Field(..., alias="intersectionName", description="Intersection Name")


class Maps(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[Map] = Field(..., alias="data", description="Data")
