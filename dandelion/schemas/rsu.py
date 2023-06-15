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


class RSUOffsetConfig(BaseModel):
    bias_x: Optional[float] = Field(None, alias="biasX", description="RSU Bias X")
    bias_y: Optional[float] = Field(None, alias="biasY", description="RSU Bias Y")
    rotation: Optional[float] = Field(None, alias="rotation", description="RSU Rotation")
    reverse: Optional[bool] = Field(None, alias="reverse", description="RSU Reverse")
    scale: Optional[float] = Field(None, alias="scale", description="RSU Scale")


# Shared properties
class RSUBase(RSUOffsetConfig):
    rsu_id: str = Field(..., alias="rsuId", description="RSU ID")
    rsu_name: str = Field(..., alias="rsuName", description="RSU Name")
    rsu_esn: str = Field(..., alias="rsuEsn", description="RSU ESN")
    rsu_ip: str = Field(..., alias="rsuIP", description="RSU IP")
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
class RSUCreate(RSUOffsetConfig):
    tmp_id: Optional[int] = Field(0, alias="tmpId", description="Temporary RSU ID")
    rsu_id: str = Field(..., alias="rsuId", description="RSU ID")
    rsu_name: str = Field(..., alias="rsuName", description="RSU Name")
    rsu_esn: str = Field(..., alias="rsuEsn", description="RSU ESN")
    rsu_ip: str = Field(..., alias="rsuIP", description="RSU IP")
    rsu_model_id: Optional[int] = Field(None, alias="rsuModelId", description="RSU Model ID")
    desc: Optional[str] = Field(None, alias="desc", description="Description")
    lat: str = Field(..., alias="lat", description="Latitude")
    lon: str = Field(..., alias="lon", description="Longitude")


# Properties to receive via API on update
class RSUUpdate(RSUOffsetConfig):
    rsu_id: Optional[str] = Field(None, alias="rsuId", description="RSU ID")
    rsu_name: Optional[str] = Field(None, alias="rsuName", description="RSU Name")
    rsu_esn: Optional[str] = Field(None, alias="rsuEsn", description="RSU ESN")
    rsu_ip: Optional[str] = Field(None, alias="rsuIP", description="RSU IP")
    rsu_model_id: Optional[int] = Field(None, alias="rsuModelId", description="RSU Model ID")
    desc: Optional[str] = Field(None, alias="desc", description="Description")
    rsu_status: Optional[str] = Field(None, alias="rsuStatus", description="RSU Status")
    enabled: Optional[bool] = Field(None, alias="enabled", description="Enable RSU or not")
    lat: Optional[str] = Field(None, alias="lat", description="Latitude")
    lon: Optional[str] = Field(None, alias="lon", description="Longitude")


class RSUUpdateWithVersion(BaseModel):
    rsu_id: Optional[str] = Field(None, alias="rsuId", description="RSU ID")
    rsu_name: Optional[str] = Field(None, alias="rsuName", description="RSU Name")
    version: Optional[str] = Field(None, alias="version", description="Version")
    location: Optional[RSULocation] = Field(None, alias="location", description="Location")
    config: Optional[Dict[str, Any]] = Field(None, alias="config", description="Config")


class RSUUpdateWithStatus(RSUUpdate):
    online_status: Optional[bool] = Field(None, alias="onlineStatus", description="Status")


class RSUUpdateWithBaseInfo(BaseModel):
    rsu_id: Optional[str] = Field(None, alias="rsuId", description="RSU ID")
    version: Optional[str] = Field(None, alias="version", description="Version")
    location: Optional[RSULocation] = Field(None, alias="location", description="Location")
    rsu_status: Optional[str] = Field(None, alias="rsuStatus", description="RSU Status")
    imei: Optional[str] = Field(None, alias="imei", description="RSU IMEI")
    icc_id: Optional[str] = Field(None, alias="iccId", description="RSU ICC ID")
    communication_type: Optional[str] = Field(
        None, alias="communicationType", description="Communication Type"
    )
    running_communication_type: Optional[str] = Field(
        None, alias="runningCommunicationType", description="Running Communication Type"
    )
    transprotocal: Optional[str] = Field(None, alias="transprotocal", description="Transprotocal")
    software_version: Optional[str] = Field(
        None, alias="softwareVersion", description="Software Version"
    )
    hardware_version: Optional[str] = Field(
        None, alias="hardwareVersion", description="Hardware Version"
    )
    depart: Optional[str] = Field(None, alias="depart", description="Organization")


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
    rsu_model_name: Optional[str] = Field(None, alias="rsuModelName", description="RSU Model Name")
    config: Optional[List[Dict[str, Any]]] = Field(
        None, alias="config", description="RSU Config RSU"
    )
    imei: Optional[str] = Field(None, alias="imei", description="IMEI")
    icc_id: Optional[str] = Field(None, alias="iccID", description="ICC ID")
    communication_type: Optional[str] = Field(
        None, alias="communicationType", description="Communication Type"
    )
    running_communication_type: Optional[str] = Field(
        None, alias="runningCommunicationType", description="Running Communication Type"
    )
    transprotocal: Optional[str] = Field(
        None, alias="transprotocal", description="RSU Transprotocal"
    )
    software_version: Optional[str] = Field(
        None, alias="softwareVersion", description="Software Version"
    )
    hardware_version: Optional[str] = Field(
        None, alias="hardwareVersion", description="Hardware Version"
    )
    depart: Optional[str] = Field(None, alias="depart", description="Organization")
    running_info: Optional[Dict[str, Any]] = Field(
        None, alias="runningInfo", description="RSU Running Info"
    )


class RunningCPU(BaseModel):
    time: Optional[str] = Field(None, alias="time", description="time")
    uti: Optional[int] = Field(None, alias="uti", description="CPU UTI")
    load: Optional[float] = Field(None, alias="load", description="CPU Load")


class RunningMEM(BaseModel):
    time: Optional[str] = Field(None, alias="time", description="time")
    total: Optional[float] = Field(None, alias="total", description="MEM Total")
    used: Optional[float] = Field(None, alias="used", description="MEM Used")


class RunningDisk(BaseModel):
    time: Optional[str] = Field(None, alias="time", description="time")
    rx_byte: Optional[float] = Field(None, alias="rxByte", description="Disk RXByte")
    wx_byte: Optional[float] = Field(None, alias="wxByte", description="Disk WXByte")


class RunningNet(BaseModel):
    time: Optional[str] = Field(None, alias="time", description="time")
    read: Optional[float] = Field(None, alias="read", description="Net Read")
    write: Optional[float] = Field(None, alias="write", description="Net Write")


class RSURunning(BaseModel):
    cpu: Optional[List[RunningCPU]] = Field(None, alias="cpu", description="CPU Info")
    mem: Optional[List[RunningMEM]] = Field(None, alias="mem", description="MEM Info")
    disk: Optional[List[RunningDisk]] = Field(None, alias="disk", description="Disk Info")
    net: Optional[List[RunningNet]] = Field(None, alias="net", description="NET Info")


class RSUs(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[RSU] = Field(..., alias="data", description="Data")
