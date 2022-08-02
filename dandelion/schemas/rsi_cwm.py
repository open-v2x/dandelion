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

<<<<<<< HEAD
from datetime import datetime
=======
>>>>>>> bd4ed84 (feat: Add RSI_CLC RSI_CWM RSI_SDS)
from typing import List, Optional

from pydantic import BaseModel, Field


class RSICWMBase(BaseModel):
    sensor_pos: Optional[Position] = Field(None, alias="sensorPos", description="Sensor Position")
    event_type: Optional[int] = Field(None, alias="eventType", description="Event Type")
    collision_type: Optional[int] = Field(
        None, alias="collisionType", description="Collision Type"
    )
    sec_mark: Optional[int] = Field(None, alias="secMark", description="Millisecond Time")
    ego_id: Optional[str] = Field(None, alias="egoId", description="EGO ID")
    ego_pos: Optional[Position] = Field(None, alias="egoPos", description="EGO Position")
    ego_heading: Optional[int] = Field(None, alias="egoHeading", description="EGO Heading")
    ego_radius: Optional[float] = Field(None, alias="egoRadius", description="EGO Radius")
    ego_length: Optional[float] = Field(None, alias="egoLength", description="EGO Length")
    ego_width: Optional[float] = Field(None, alias="egoWidth", description="EGO Width")
    ego_kinematics_info: Optional[KinematicsInfo] = Field(
        None, alias="egoKinematicsInfo", description="EGO KinematicsInfo"
    )
    other_id: Optional[str] = Field(None, alias="otherId", description="Other ID")
    other_pos: Optional[Position] = Field(None, alias="otherPos", description="Other Position")
    other_heading: Optional[int] = Field(None, alias="otherHeading", description="Other Heading")
    other_radius: Optional[float] = Field(None, alias="otherRadius", description="Other Radius")
    other_length: Optional[float] = Field(None, alias="otherLength", description="Other Length")
    other_width: Optional[float] = Field(None, alias="otherWidth", description="Other Width")
    other_kinematics_info: Optional[KinematicsInfo] = Field(
        None, alias="otherKinematicsInfo", description="Other KinematicsInfo"
    )


class Position(BaseModel):
    lon: int = Field(..., alias="lon", description="Longitude")
    lat: int = Field(..., alias="lat", description="Latitude")
    ele: Optional[int] = Field(None, alias="ele", description="Elevation")


class KinematicsInfo(BaseModel):
    speed: float = Field(..., alias="speed", description="Speed")
    accelerate: float = Field(..., alias="accelerate", description="Accelerate")
    angular_speed: int = Field(..., alias="angularSpeed", description="Angular Speed")


class RSICWMCreate(RSICWMBase):
    """"""


class RSICWMInDBBase(RSICWMBase):
    id: int = Field(..., alias="id", description="CWM ID")
<<<<<<< HEAD
    create_time: datetime = Field(..., alias="createTime", description="Create Time")
=======
>>>>>>> bd4ed84 (feat: Add RSI_CLC RSI_CWM RSI_SDS)

    class Config:
        orm_mode = True


# Additional properties to return via API
class RSICWM(RSICWMInDBBase):
    """"""


class RSICWMs(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[RSICWM] = Field(..., alias="data", description="Data")
