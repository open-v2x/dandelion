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

from typing import Optional

from pydantic import BaseModel, Field


class RSUOnlineRateBase(BaseModel):
    online: int = Field(..., alias="online", description="Online")
    offline: int = Field(..., alias="offline", description="Offline")
    not_register: int = Field(..., alias="notRegister", description="Not Register")


class CameraOnlineRateBase(RSUOnlineRateBase):
    """"""


class RadarOnlineRateBase(RSUOnlineRateBase):
    """"""


class LidarOnlineRateBase(RSUOnlineRateBase):
    """"""


class SpatOnlineRateBase(RSUOnlineRateBase):
    """"""


class OnlineRateBase(BaseModel):
    rsu: RSUOnlineRateBase = Field(..., alias="rsu", description="RSU Online Rate")
    camera: CameraOnlineRateBase = Field(..., alias="camera", description="Camera Online Rate")
    radar: RadarOnlineRateBase = Field(..., alias="radar", description="Radar Online Rate")
    lidar: LidarOnlineRateBase = Field(..., alias="lidar", description="Lidar Online Rate")
    spat: SpatOnlineRateBase = Field(..., alias="spat", description="Spat Online Rate")


class OnlineRate(BaseModel):
    data: OnlineRateBase = Field(..., alias="data", description="Online Rate")


class RouteInfo(BaseModel):
    vehicle_total: int = Field(..., alias="vehicleTotal", description="Vehicle Total")
    average_speed: int = Field(..., alias="averageSpeed", description="Average Speed")
    pedestrian_total: int = Field(..., alias="pedestrianTotal", description="Pedestrian Total")
    congestion: str = Field(..., alias="congestion", description="Congestion")


class RouteInfoCreate(BaseModel):
    rsu_esn: str = Field(..., alias="rsuEsn", description="RSU ESN")
    vehicle_total: Optional[int] = Field(0, alias="vehicleTotal", description="Vehicle Total")
    average_speed: Optional[int] = Field(0, alias="averageSpeed", description="Average Speed")
    pedestrian_total: Optional[int] = Field(
        0, alias="pedestrianTotal", description="Pedestrian Total"
    )
    congestion: Optional[str] = Field("Unknown", alias="congestion", description="Congestion")
