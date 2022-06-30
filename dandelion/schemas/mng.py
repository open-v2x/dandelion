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
from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class LogLevel(str, Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    NOLog = "NOLog"


class Reboot(str, Enum):
    not_reboot = "not_reboot"
    reboot = "reboot"


class AddressChg(BaseModel):
    cssUrl: str = Field(..., alias="cssUrl", description="CSS URL")
    time: int = Field(..., alias="time", description="Time")


# Shared properties
class MNGBase(BaseModel):
    """"""


# Properties to receive via API on creation
class MNGCreate(BaseModel):
    """"""


# Properties to receive via API on update
class MNGUpdate(MNGBase):
    heartbeat_rate: int = Field(..., alias="hbRate", description="Heartbeat Rate")
    running_info_rate: int = Field(..., alias="runningInfoRate", description="Running Info Rate")
    address_change: AddressChg = Field(..., alias="addressChg", description="Address Change")
    log_level: LogLevel = Field(..., alias="logLevel", description="Log Level")
    reboot: Reboot = Field(..., alias="reboot", description="Reboot")
    extend_config: str = Field(..., alias="extendConfig", description="Extend Config")


class MNGInDBBase(MNGBase):
    id: int = Field(..., alias="id", description="MNG ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class MNG(MNGInDBBase):
    rsu_name: str = Field(..., alias="rsuName", description="RSU Name")
    rsu_esn: str = Field(..., alias="rsuEsn", description="RSU ESN")
    heartbeat_rate: int = Field(..., alias="hbRate", description="Heartbeat Rate")
    running_info_rate: int = Field(..., alias="runningInfoRate", description="Running Info Rate")
    address_change: AddressChg = Field(..., alias="addressChg", description="Address Change")
    log_level: LogLevel = Field(..., alias="logLevel", description="Log Level")
    reboot: Reboot = Field(..., alias="reboot", description="Reboot")
    extend_config: str = Field(..., alias="extendConfig", description="Extend Config")
    create_time: datetime = Field(..., alias="createTime", description="Create Time")


class MNGs(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[MNG] = Field(..., alias="data", description="Data")


class MNGCopy(BaseModel):
    rsus: List[int] = Field(..., alias="rsus", description="RSUs")
