# Copyright 2023 99Cloud, Inc. All Rights Reserved.
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
class EndpointBase(BaseModel):
    """"""


# Properties to receive via API on creation
class EndpointCreate(EndpointBase):
    """"""

    service_id: int = Field(..., alias="service_id", description="Service ID")
    enabled: bool = Field(..., alias="enabled", description="Endpoint enabled flag")
    url: str = Field(..., alias="url", description="Endpoint url")


# Properties to receive via API on update
class EndpointUpdate(EndpointBase):
    """"""

    service_id: int = Field(..., alias="service_id", description="Service ID")
    enabled: bool = Field(..., alias="enabled", description="Endpoint enabled flag")
    url: str = Field(..., alias="url", description="Endpoint url")


class EndpointInDBBase(EndpointBase):
    id: int = Field(..., alias="id", description="Endpoint ID")

    class Config:
        orm_mode = True


class EndpointCreateAll(EndpointInDBBase):
    service_id: int = Field(..., alias="service_id", description="Service ID")
    enabled: bool = Field(..., alias="enabled", description="Endpoint enabled flag")
    url: str = Field(..., alias="url", description="Endpoint url")


class EndpointGET(EndpointBase):
    """"""

    id: Optional[int] = Field(None, alias="id", description="Endpoint id")
    service_id: int = Field(..., alias="service_id", description="Service ID")
    enabled: bool = Field(..., alias="enabled", description="Endpoint enabled flag")
    url: str = Field(..., alias="url", description="Endpoint url")


class Endpoints(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[EndpointCreateAll] = Field(..., alias="data", description="Data")
