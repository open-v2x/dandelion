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


class RSULocation(BaseModel):
    lat: Optional[float] = Field(None, alias="lat", description="Latitude")
    lon: Optional[float] = Field(None, alias="lon", description="Longitude")


class RSUConfigRSUInRSU(BaseModel):
    id: int = Field(..., alias="id", description="ID")
    status: bool = Field(..., alias="status", description="Status")
    rsu_id: int = Field(..., alias="rsu_id", description="RSU ID")
    rsu_config_id: int = Field(..., alias="rsu_config_id", description="RSU Config ID")
    create_time: datetime = Field(..., alias="create_time", description="Create Time")


# Shared properties
class RSUBase(BaseModel):
    rsu_id: str = Field(..., alias="rsuId", description="RSU ID")
    rsu_name: str = Field(..., alias="rsuName", description="RSU Name")
    rsu_esn: str = Field(..., alias="rsuEsn", description="RSU ESN")
    rsu_ip: str = Field(..., alias="rsuIP", description="RSU IP")
    country_code: str = Field(..., alias="countryCode", description="Country Code")
    country_name: str = Field(..., alias="countryName", description="Country Name")
    province_code: str = Field(..., alias="provinceCode", description="Province Code")
    province_name: str = Field(..., alias="provinceName", description="Province Name")
    city_code: str = Field(..., alias="cityCode", description="City Code")
    city_name: str = Field(..., alias="cityName", description="City Name")
    area_code: str = Field(..., alias="areaCode", description="Area Code")
    area_name: str = Field(..., alias="areaName", description="Area Name")
    address: str = Field(..., alias="address", description="Address")
    rsu_status: str = Field(..., alias="rsuStatus", description="RSU Status")
    enabled: Optional[bool] = Field(None, alias="enabled", description="Enable RSU or not")
    online_status: bool = Field(..., alias="onlineStatus", description="Online Status")
    rsu_model_id: Optional[int] = Field(None, alias="rsuModelId", description="RSU Model ID")
    desc: Optional[str] = Field(None, alias="desc", description="Description")
    create_time: datetime = Field(..., alias="createTime", description="Create Time")
    version: Optional[str] = Field(None, alias="version", description="Version")
    update_time: datetime = Field(..., alias="updateTime", description="Update Time")
    location: Optional[RSULocation] = Field(None, alias="location", description="Location")


# Properties to receive via API on creation
class RSUCreate(BaseModel):
    tmp_id: Optional[int] = Field(0, alias="tmpId", description="Temporary RSU ID")
    rsu_id: str = Field(..., alias="rsuId", description="RSU ID")
    rsu_name: str = Field(..., alias="rsuName", description="RSU Name")
    rsu_esn: str = Field(..., alias="rsuEsn", description="RSU ESN")
    rsu_ip: str = Field(..., alias="rsuIP", description="RSU IP")
    area_code: str = Field(..., alias="areaCode", description="Area Code")
    address: str = Field(..., alias="address", description="Address")
    rsu_model_id: Optional[int] = Field(None, alias="rsuModelId", description="RSU Model ID")
    desc: Optional[str] = Field(None, alias="desc", description="Description")


# Properties to receive via API on update
class RSUUpdate(BaseModel):
    rsu_id: Optional[str] = Field(None, alias="rsuId", description="RSU ID")
    rsu_name: Optional[str] = Field(None, alias="rsuName", description="RSU Name")
    rsu_esn: Optional[str] = Field(None, alias="rsuEsn", description="RSU ESN")
    rsu_ip: Optional[str] = Field(None, alias="rsuIP", description="RSU IP")
    area_code: Optional[str] = Field(None, alias="areaCode", description="Area Code")
    address: Optional[str] = Field(None, alias="address", description="Address")
    rsu_model_id: Optional[int] = Field(None, alias="rsuModelId", description="RSU Model ID")
    desc: Optional[str] = Field(None, alias="desc", description="Description")
    rsu_status: Optional[str] = Field(None, alias="rsuStatus", description="RSU Status")
    enabled: Optional[bool] = Field(None, alias="enabled", description="Enable RSU or not")


class RSUUpdateWithVersion(BaseModel):
    rsu_id: Optional[str] = Field(None, alias="rsuId", description="RSU ID")
    rsu_name: Optional[str] = Field(None, alias="rsuName", description="RSU Name")
    version: Optional[str] = Field(None, alias="version", description="Version")
    location: Optional[RSULocation] = Field(None, alias="location", description="Location")
    config: Optional[Dict[str, Any]] = Field(None, alias="config", description="Config")


class RSUUpdateWithStatus(RSUUpdate):
    online_status: Optional[bool] = Field(None, alias="onlineStatus", description="Status")


class RSUInDBBase(RSUBase):
    id: int = Field(..., alias="id", description="RSU ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class RSU(RSUInDBBase):
    config: Optional[Dict[str, Any]] = Field(None, alias="config", description="Config")
    delivery_status: Optional[int] = Field(
        None, alias="deliveryStatus", description="Delivery Status"
    )


class RSUDetail(RSUInDBBase):
    config: List[RSUConfigRSUInRSU] = Field(..., alias="config", description="RSU Config RSU")


class RSUs(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[RSU] = Field(..., alias="data", description="Data")
