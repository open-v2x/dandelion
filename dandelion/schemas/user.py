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
class UserBase(BaseModel):
    username: Optional[str] = Field(None, alias="username", description="Username")
    is_active: Optional[bool] = Field(True, alias="is_active", description="Is active")


# Properties to receive via API on creation
class UserCreate(UserBase):
    username: str = Field(..., alias="username", description="Username")
    password: str = Field(..., alias="password", description="Password")


# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = Field(None, alias="password", description="Password")


class UserInDBBase(UserBase):
    id: Optional[int] = Field(None, alias="id", description="User ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class User(UserInDBBase):
    """"""
