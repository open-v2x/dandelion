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

from typing import Optional

from pydantic import BaseModel, Field


# Shared properties
class RSMBase(BaseModel):
    """"""


# Properties to receive via API on creation
class RSMCreate(BaseModel):
    ref_pos: Optional[str] = Field(None, alias="refPos", description="Ref pos")


# Properties to receive via API on update
class RSMUpdate(RSMBase):
    """"""


class RSMInDBBase(RSMBase):
    id: int = Field(..., alias="id", description="RSM ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class RSM(RSMInDBBase):
    """"""


class RSMs(BaseModel):
    """"""
