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
class RadarCameraBase(BaseModel):
    """"""

    name: str = Field(..., alias="name", description="RadarCamera Name")
    sn: str = Field(..., alias="sn", description="RadarCamera SN")
    lng: str = Field(..., alias="lng", description="Longitude")
    lat: str = Field(..., alias="lat", description="Latitude")
    elevation: str = Field(..., alias="elevation", description="Elevation")
    towards: str = Field(..., alias="towards", description="Towards")
    point: str = Field(..., alias="point", description="point")
    pole: str = Field(..., alias="pole", description="pole")
    radar_camera_ip: str = Field(..., alias="radarCameraIP", description="RadarCamera IP")
    video_stream_address: str = Field(
        ..., alias="videoStreamAddress", description="video stream address"
    )
    rsu_id: Optional[int] = Field(None, alias="rsuID", description="RSU ID")
    desc: Optional[str] = Field("", alias="desc", description="Description")


# Properties to receive via API on creation
class RadarCameraCreate(RadarCameraBase):
    """"""


# Properties to receive via API on update
class RadarCameraUpdate(BaseModel):
    name: Optional[str] = Field(None, alias="name", description="RadarCamera Name")
    sn: Optional[str] = Field(None, alias="sn", description="RadarCamera SN")
    lng: Optional[str] = Field(None, alias="lng", description="Longitude")
    lat: Optional[str] = Field(None, alias="lat", description="Latitude")
    elevation: Optional[str] = Field(None, alias="elevation", description="Elevation")
    towards: Optional[str] = Field(None, alias="towards", description="Towards")
    point: Optional[str] = Field(None, alias="point", description="point")
    pole: Optional[str] = Field(None, alias="pole", description="pole")
    radar_camera_ip: Optional[str] = Field(
        None, alias="radarCameraIP", description="RadarCamera IP"
    )
    video_stream_address: Optional[str] = Field(
        None, alias="videoStreamAddress", description="video stream address"
    )
    rsu_id: Optional[int] = Field(None, alias="rsuID", description="RSU ID")
    desc: Optional[str] = Field("", alias="desc", description="Description")
    enabled: Optional[bool] = Field(None, alias="enabled", description="enabled")


class RadarCameraInDBBase(RadarCameraBase):
    id: int = Field(..., alias="id", description="RadarCamera ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class RadarCamera(RadarCameraInDBBase):
    status: bool = Field(..., alias="status", description="Status")
    rsu_name: Optional[str] = Field(None, alias="rsuName", description="RSU Name")
    create_time: datetime = Field(..., alias="createTime", description="Create Time")
    enabled: bool = Field(..., alias="enabled", description="Enabled radar camera or not")


class RadarCameras(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[RadarCamera] = Field(..., alias="data", description="Data")
