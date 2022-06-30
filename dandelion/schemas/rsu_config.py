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
from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from .rsu import RSU


class SampleMode(str, Enum):
    by_all = "ByAll"
    by_id = "ByID"


class BSM(BaseModel):
    sample_mode: Optional[SampleMode] = Field(
        None, alias="sampleMode", description="The sample mode of the BSM."
    )
    sample_rate: Optional[int] = Field(
        None, alias="sampleRate", description="The sample rate of the BSM."
    )
    up_limit: Optional[int] = Field(
        None, alias="upLimit", description="The upper limit of the BSM."
    )
    up_filters: Optional[List[Dict[str, str]]] = Field(
        None, alias="upFilters", description="The upper filters of the BSM."
    )


class RSI(BaseModel):
    up_filters: Optional[List[Dict[str, str]]] = Field(
        None, alias="upFilters", description="The upper filters of the RSI."
    )


class RSM(BaseModel):
    up_limit: Optional[int] = Field(
        None, alias="upLimit", description="The upper limit of the RSM."
    )
    up_filters: Optional[List[Dict[str, str]]] = Field(
        None, alias="upFilters", description="The upper filters of the RSM."
    )


class MAP(BaseModel):
    up_limit: Optional[int] = Field(
        None, alias="upLimit", description="The upper limit of the MAP."
    )
    up_filters: Optional[List[Dict[str, str]]] = Field(
        None, alias="upFilters", description="The upper filters of the MAP."
    )


class SPAT(BaseModel):
    up_limit: Optional[int] = Field(
        None, alias="upLimit", description="The upper limit of the SPAT."
    )
    up_filters: Optional[List[Dict[str, str]]] = Field(
        None, alias="upFilters", description="The upper filters of the SPAT."
    )


# Shared properties
class RSUConfigBase(BaseModel):
    """"""


# Properties to receive via API on creation
class RSUConfigCreate(BaseModel):
    name: str = Field(..., alias="name", description="RSU Config name")
    bsm: BSM = Field(..., alias="bsm", description="BSM")
    rsi: RSI = Field(..., alias="rsi", description="RSI")
    rsm: RSM = Field(..., alias="rsm", description="RSM")
    map: MAP = Field(..., alias="map", description="MAP")
    spat: Optional[SPAT] = Field(None, alias="spat", description="SPAT")
    rsus: Optional[List[int]] = Field(None, alias="rsus", description="RSUs")


# Properties to receive via API on update
class RSUConfigUpdate(RSUConfigBase):
    name: str = Field(..., alias="name", description="RSU Config name")
    bsm: BSM = Field(..., alias="bsm", description="BSM")
    rsi: RSI = Field(..., alias="rsi", description="RSI")
    rsm: RSM = Field(..., alias="rsm", description="RSM")
    map: MAP = Field(..., alias="map", description="MAP")
    spat: Optional[SPAT] = Field(None, alias="spat", description="SPAT")
    rsus: Optional[List[int]] = Field(None, alias="rsus", description="RSUs")


class RSUConfigInDBBase(RSUConfigBase):
    id: int = Field(..., alias="id", description="RSU Config ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class RSUConfig(RSUConfigInDBBase):
    name: str = Field(..., alias="name", description="RSU Config name")
    bsm_config: Optional[BSM] = Field(None, alias="bsmConfig", description="BSM")
    rsi_config: Optional[RSI] = Field(None, alias="rsiConfig", description="RSI")
    rsm_config: Optional[RSM] = Field(None, alias="rsmConfig", description="RSM")
    map_config: Optional[MAP] = Field(None, alias="mapConfig", description="MAP")
    spat_config: Optional[SPAT] = Field(None, alias="spatConfig", description="SPAT")
    create_time: datetime = Field(..., alias="createTime", description="Create time")


class RSUConfigWithRSUs(RSUConfig):
    rsus: List[RSU] = Field(..., alias="rsus", description="RSUs")


class RSUConfigs(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[RSUConfig] = Field(..., alias="data", description="Data")
