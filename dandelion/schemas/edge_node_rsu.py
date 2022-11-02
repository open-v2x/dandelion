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

from typing import List, Optional

from pydantic import BaseModel, Field


# Shared properties
class EdgeNodeRSUBase(BaseModel):
    name: Optional[str] = Field(None, alias="name", description="RSU Name")
    esn: Optional[str] = Field(None, alias="esn", description="RSU ESN")
    location: Optional[Location] = Field(None, alias="location", description="Location")


class Location(BaseModel):
    lat: Optional[float] = Field(None, alias="lat", description="Latitude")
    lon: Optional[float] = Field(None, alias="lon", description="Longitude")


# Properties to receive via API on creation
class EdgeNodeRSUCreate(EdgeNodeRSUBase):
    area_code: Optional[str] = Field(None, alias="areaCode", description="Area Code")
    edge_node_id: Optional[int] = Field(None, alias="edgeNodeID", description="Edge Node ID")
    edge_rsu_id: Optional[int] = Field(None, alias="edgeRsuID", description="Edge Rsu ID")


# Properties to receive via API on update
class EdgeNodeRSUUpdate(EdgeNodeRSUBase):
    area_code: Optional[str] = Field(None, alias="areaCode", description="Area Code")
    edge_node_id: Optional[int] = Field(None, alias="edgeNodeID", description="Edge Node ID")
    edge_rsu_id: Optional[int] = Field(None, alias="edgeRsuID", description="Edge Rsu ID")


class EdgeNodeRSUInDBBase(EdgeNodeRSUBase):
    id: int = Field(..., alias="id", description="RSU ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class EdgeNodeRSU(EdgeNodeRSUInDBBase):
    """"""


class EdgeNodeRSUs(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[EdgeNodeRSU] = Field(..., alias="data", description="Data")
