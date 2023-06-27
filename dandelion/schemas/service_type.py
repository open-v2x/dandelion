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
class ServiceTypeBase(BaseModel):
    """"""


# Properties to receive via API on creation
class ServiceTypeCreate(ServiceTypeBase):
    """"""

    name: str = Field(..., alias="name", description="Service type name")
    description: Optional[str] = Field(
        None, alias="description", description="Service type description"
    )


# Properties to receive via API on update
class ServiceTypeUpdate(ServiceTypeBase):
    """"""

    name: str = Field(..., alias="name", description="Service type name")
    description: Optional[str] = Field(
        None, alias="description", description="Service type description"
    )


class ServiceTypeInDBBase(ServiceTypeBase):
    id: int = Field(..., alias="id", description="Service type ID")

    class Config:
        orm_mode = True


class ServiceTypeCreateAll(ServiceTypeInDBBase):
    name: str = Field(..., alias="name", description="Service type name")
    description: Optional[str] = Field(
        None, alias="description", description="Service type description"
    )


class ServiceTypeGET(ServiceTypeBase):
    """"""

    id: Optional[int] = Field(None, alias="id", description="Service type id")
    name: str = Field(..., alias="name", description="Service type name")
    description: Optional[str] = Field(
        None, alias="description", description="Service type description"
    )


class ServiceTypes(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[ServiceTypeCreateAll] = Field(..., alias="data", description="Data")
