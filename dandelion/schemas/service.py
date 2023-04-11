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
class ServiceBase(BaseModel):
    """"""


# Properties to receive via API on creation
class ServiceCreate(ServiceBase):
    """"""

    name: str = Field(..., alias="name", description="Service name")
    type_id: int = Field(..., alias="type_id", description="Service type ID")
    vendor: str = Field(..., alias="vendor", description="Service vendor")
    description: str = Field(..., alias="description", description="Service description")


# Properties to receive via API on update
class ServiceUpdate(ServiceBase):
    """"""

    name: str = Field(..., alias="name", description="Service name")
    type_id: int = Field(..., alias="type_id", description="Service type ID")
    vendor: str = Field(..., alias="vendor", description="Service vendor")
    description: str = Field(..., alias="description", description="Service description")


class ServiceInDBBase(ServiceBase):
    id: int = Field(..., alias="id", description="Service ID")

    class Config:
        orm_mode = True


class ServiceCreateAll(ServiceInDBBase):
    name: str = Field(..., alias="name", description="Service name")
    type_id: int = Field(..., alias="type_id", description="Service type ID")
    vendor: str = Field(..., alias="vendor", description="Service vendor")
    description: str = Field(..., alias="description", description="Service description")


class ServiceGET(ServiceBase):
    """"""

    id: Optional[int] = Field(None, alias="id", description="Service id")
    name: str = Field(..., alias="name", description="Service name")
    type_id: int = Field(..., alias="type_id", description="Service type ID")
    vendor: str = Field(..., alias="vendor", description="Service vendor")
    description: str = Field(..., alias="description", description="Service description")


class Services(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[ServiceCreateAll] = Field(..., alias="data", description="Data")
