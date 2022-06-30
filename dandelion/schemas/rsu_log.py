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


class TransProtocal(str, Enum):
    http = "http"
    https = "https"
    ftp = "ftp"
    sftp = "sftp"
    other = "other"


class RSUInRSULog(BaseModel):
    id: int = Field(..., alias="id", description="ID")
    rsu_name: str = Field(..., alias="rsuName", description="RSU Name")
    rsu_esn: str = Field(..., alias="rsuEsn", description="RSU ESN")


# Shared properties
class RSULogBase(BaseModel):
    """"""


# Properties to receive via API on creation
class RSULogCreate(BaseModel):
    upload_url: str = Field(..., alias="uploadUrl", description="Upload URL")
    user_id: str = Field(..., alias="userId", description="User ID")
    password: str = Field(..., alias="password", description="Password")
    transprotocal: TransProtocal = Field(..., alias="transprotocal", description="Transprotocal")
    rsus: List[int] = Field(..., alias="rsus", description="RSUs")


# Properties to receive via API on update
class RSULogUpdate(RSULogBase):
    upload_url: str = Field(..., alias="uploadUrl", description="Upload URL")
    user_id: str = Field(..., alias="userId", description="User ID")
    password: str = Field(..., alias="password", description="Password")
    transprotocal: TransProtocal = Field(..., alias="transprotocal", description="Transprotocal")
    rsus: List[int] = Field(..., alias="rsus", description="RSUs")


class RSULogInDBBase(RSULogBase):
    id: int = Field(..., alias="id", description="RSU Log ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class RSULog(RSULogInDBBase):
    upload_url: str = Field(..., alias="uploadUrl", description="Upload URL")
    user_id: str = Field(..., alias="userId", description="User ID")
    password: str = Field(..., alias="password", description="Password")
    transprotocal: TransProtocal = Field(..., alias="transprotocal", description="Transprotocal")
    create_time: datetime = Field(..., alias="createTime", description="Create Time")
    rsus: List[RSUInRSULog] = Field(..., alias="rsus", description="RSUs")


class RSULogs(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[RSULog] = Field(..., alias="data", description="Data")
