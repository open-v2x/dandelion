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

from pydantic import BaseModel, Field


# Shared properties
class RSUConfigRSUBase(BaseModel):
    """"""


# Properties to receive via API on creation
class RSUConfigRSUCreate(BaseModel):
    """"""


# Properties to receive via API on update
class RSUConfigRSUUpdate(RSUConfigRSUBase):
    """"""


class RSUConfigRSUInDBBase(RSUConfigRSUBase):
    id: int = Field(..., alias="id", description="RSU Config RSU ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class RSUConfigRSU(RSUConfigRSUInDBBase):
    """"""


class RSUConfigRSUs(BaseModel):
    """"""
