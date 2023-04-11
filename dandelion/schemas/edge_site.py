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

from pydantic import BaseModel, Field, HttpUrl


# Shared properties
class EdgeSiteBase(BaseModel):
    name: str = Field(..., alias="name", description="Edge Site Name")
    edge_site_dandelion_endpoint: HttpUrl = Field(
        ..., alias="edgeSiteDandelionEndpoint", description="Edge Site Dandelion Endpoint"
    )
    area_code: Optional[str] = Field(None, alias="areaCode", description="Edge Site Area Code")
    desc: Optional[str] = Field(None, alias="desc", description="Edge Site desc")


# Properties to receive via API on creation
class EdgeSiteCreate(EdgeSiteBase):
    """"""

    center_dandelion_endpoint: HttpUrl = Field(
        ..., alias="centerDandelionEndpoint", description="Edge Site Dandelion Endpoint"
    )


# Properties to receive via API on update
class EdgeSiteUpdate(BaseModel):
    """"""

    name: Optional[str] = Field(None, alias="name", description="Edge Site Name")


class EdgeSiteInDBBase(EdgeSiteBase):
    id: int = Field(..., alias="id", description="Edge Site ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class EdgeSite(EdgeSiteInDBBase):
    """"""


class EdgeSites(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[EdgeSite] = Field(..., alias="data", description="Data")
