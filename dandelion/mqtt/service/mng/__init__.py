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

from logging import LoggerAdapter
from typing import Any, Dict

from oslo_log import log

from dandelion.mqtt import send_msg
from dandelion.mqtt.topic.v2x_rsu import v2x_rsu_mng_down

LOG: LoggerAdapter = log.getLogger(__name__)


def mng_down(rsu_esn: str, data: Dict[str, Any]) -> None:
    LOG.info(f"mng_down: rsu_esn={rsu_esn}, data={data}")
    send_msg(v2x_rsu_mng_down(rsu_esn), data)
