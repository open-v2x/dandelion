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
class EndpointMetadataBase(BaseModel):
    """"""


# Properties to receive via API on creation
class EndpointMetadataCreate(EndpointMetadataBase):
    """"""

    endpoint_id: int = Field(..., alias="endpoint_id", description="Endpoint ID")
    key: str = Field(..., alias="key", description="EndpointMetadata key")
    value: str = Field(..., alias="value", description="EndpointMetadata value")


# Properties to receive via API on update
class EndpointMetadataUpdate(EndpointMetadataBase):
    """"""

    endpoint_id: int = Field(..., alias="endpoint_id", description="Endpoint ID")
    key: str = Field(..., alias="key", description="EndpointMetadata key")
    value: str = Field(..., alias="value", description="EndpointMetadata value")


class EndpointMetadataInDBBase(EndpointMetadataBase):
    id: int = Field(..., alias="id", description="EndpointMetadata ID")

    class Config:
        orm_mode = True


class EndpointMetadataCreateAll(EndpointMetadataInDBBase):
    endpoint_id: int = Field(..., alias="endpoint_id", description="Endpoint ID")
    key: str = Field(..., alias="key", description="EndpointMetadata key")
    value: str = Field(..., alias="value", description="EndpointMetadata value")


class EndpointMetadataGET(EndpointMetadataBase):
    """"""

    id: Optional[int] = Field(None, alias="id", description="EndpointMetadata id")
    endpoint_id: int = Field(..., alias="endpoint_id", description="Endpoint ID")
    key: str = Field(..., alias="key", description="EndpointMetadata key")
    value: str = Field(..., alias="value", description="EndpointMetadata value")


class EndpointMetadatas(BaseModel):
    total: int = Field(..., alias="total", description="Total")
    data: List[EndpointMetadataCreateAll] = Field(..., alias="data", description="Data")
