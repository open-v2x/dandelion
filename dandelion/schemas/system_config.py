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


class SystemConfigBase(BaseModel):
    name: Optional[str] = Field(None, alias="name", description="Site Name")
    mqtt_config: Optional[MQTTConfig] = Field(None, alias="mqtt_config", description="MQTT Config")
    area_code: Optional[str] = Field(None, alias="area_code", description="Area Code")


class MQTTConfig(BaseModel):
    host: Optional[str] = Field(None, alias="host", description="MQTT Host")
    port: Optional[int] = Field(None, alias="port", description="MQTT Port")
    username: Optional[str] = Field(None, alias="username", description="Username")
    password: Optional[str] = Field(None, alias="password", description="Password")


class SystemConfigCreate(SystemConfigBase):
    """"""

    local_ip: Optional[str] = Field(None, alias="local_ip", description="Local IP")


class SystemConfigUpdateNodeId(BaseModel):
    node_id: int = Field(..., alias="nodeID", description="Edge Node ID")


class SystemConfigInDBBase(SystemConfigBase):
    id: int = Field(..., alias="id", description="Config ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class SystemConfig(SystemConfigInDBBase):
    mode: Optional[str] = Field(None, alias="mode", description="Node Mode")
