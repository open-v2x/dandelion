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
from typing import List, Optional

from pydantic import BaseModel, Field


# Shared properties
class CameraBase(BaseModel):
    """"""


# Properties to receive via API on creation
class CameraCreate(BaseModel):
    sn: str = Field(..., alias="sn", description="SN")
    name: str = Field(..., alias="name", description="Name")
    stream_url: str = Field(..., alias="streamUrl", description="Stream URL")
    lng: float = Field(..., alias="lng", description="Lng")
    lat: float = Field(..., alias="lat", description="Lat")
    elevation: float = Field(..., alias="elevation", description="Elevation")
    towards: float = Field(..., alias="towards", description="Towards")
    rsu_id: Optional[int] = Field(None, alias="rsuId", description="RSU ID")
    desc: Optional[str] = Field(None, alias="desc", description="Description")


# Properties to receive via API on update
class CameraUpdate(CameraBase):
    sn: Optional[str] = Field(None, alias="sn", description="SN")
    name: Optional[str] = Field(None, alias="name", description="Name")
    stream_url: Optional[str] = Field(None, alias="streamUrl", description="Stream URL")
    lng: Optional[float] = Field(None, alias="lng", description="Lng")
    lat: Optional[float] = Field(None, alias="lat", description="Lat")
    elevation: Optional[float] = Field(None, alias="elevation", description="Elevation")
    towards: Optional[float] = Field(None, alias="towards", description="Towards")
    rsu_id: Optional[int] = Field(None, alias="rsuId", description="RSU ID")
    desc: Optional[str] = Field(None, alias="desc", description="Description")
    enabled: Optional[bool] = Field(None, alias="enabled", description="enabled")


class CameraInDBBase(CameraBase):
    id: int = Field(..., alias="id", description="Camera ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class Camera(CameraInDBBase):
    sn: str = Field(..., alias="sn", description="SN")
    name: str = Field(..., alias="name", description="Name")
    stream_url: str = Field(..., alias="streamUrl", description="Stream URL")
    lng: float = Field(..., alias="lng", description="Lng")
    lat: float = Field(..., alias="lat", description="Lat")
    elevation: float = Field(..., alias="elevation", description="Elevation")
    towards: float = Field(..., alias="towards", description="Towards")
    rsu_id: Optional[int] = Field(None, alias="rsuId", description="RSU ID")
    rsu_name: Optional[str] = Field(None, alias="rsuName", description="RSU Name")
    desc: str = Field(..., alias="desc", description="Description")
    create_time: datetime = Field(..., alias="createTime", description="Create Time")
    enabled: bool = Field(..., alias="enabled", description="Enabled camera or not")


class Cameras(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[Camera] = Field(..., alias="data", description="Data")
