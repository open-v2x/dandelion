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


class RunningInfo(BaseModel):
    cpu: Optional[CPUInfo] = Field(None, alias="cpu", description="CPU Info")
    mem: Optional[MEMInfo] = Field(None, alias="mem", description="MEM Info")
    disk: Optional[DiskInfo] = Field(None, alias="disk", description="Disk Info")
    net: Optional[NETInfo] = Field(None, alias="net", description="Net Info")


class CPUInfo(BaseModel):
    load: Optional[float] = Field(None, alias="load", description="CPU Load")
    uti: Optional[str] = Field(None, alias="uti", description="CPU Utilization")


class MEMInfo(BaseModel):
    total: Optional[float] = Field(None, alias="total", description="MEM Total")
    used: Optional[float] = Field(None, alias="used", description="MEM Used")
    free: Optional[float] = Field(None, alias="free", description="MEM Free")


class DiskInfo(BaseModel):
    total: Optional[float] = Field(None, alias="total", description="Disk Total(M)")
    used: Optional[float] = Field(None, alias="used", description="Disk Used(M)")
    free: Optional[float] = Field(None, alias="free", description="Disk Free(M)")
    tps: Optional[int] = Field(None, alias="tps", description="IOs per second")
    write: Optional[float] = Field(None, alias="write", description="Writes per second(K)")
    read: Optional[float] = Field(None, alias="read", description="Reads per second(K)")


class NETInfo(BaseModel):
    rx: Optional[int] = Field(
        None, alias="rx", description="Number of packets received per second"
    )
    tx: Optional[int] = Field(None, alias="tx", description="Number of packets sent per second")
    rx_byte: Optional[float] = Field(None, alias="rxByte", description="Bytes received per second")
    tx_byte: Optional[float] = Field(None, alias="txByte", description="Bytes sent per second")


class RSURunningInfoCreate(RunningInfo):
    """"""
