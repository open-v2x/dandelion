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
    mqtt_config: MQTTConfig = Field(..., alias="mqttConfig", description="MQTT Config")


class MQTTConfig(BaseModel):
    host: str = Field(..., alias="host", description="MQTT Host")
    port: int = Field(..., alias="port", description="MQTT Port")
    username: str = Field(..., alias="username", description="Username")
    password: str = Field(..., alias="password", description="Password")


class SystemConfigCreate(SystemConfigBase):
    """"""

    edge_site_external_ip: Optional[str] = Field(
        None, alias="edgeSiteExternalIP", description="Edge Site External IP"
    )
    center_dandelion_endpoint: str = Field(
        ..., alias="centerDandelionEndpoint", description="Center Dandelion Endpoint"
    )
    edge_site_id: int = Field(..., alias="edgeSiteID", description="Edge Site ID")


class SystemConfigInDBBase(SystemConfigBase):
    id: int = Field(..., alias="id", description="Config ID")

    class Config:
        orm_mode = True


# Additional properties to return via API
class SystemConfig(SystemConfigInDBBase):
    edge_site_id: Optional[int] = Field(None, alias="edgeSiteID", description="Edge Site ID")
    mode: Optional[str] = Field(None, alias="mode", description="Node Mode")
