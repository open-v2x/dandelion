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
from typing import Any, Dict, Optional

from oslo_log import log

from dandelion.mqtt import send_msg
from dandelion.mqtt.topic import V2X_RSU_LOG_UP, v2x_rsu_log_conf_down

LOG: LoggerAdapter = log.getLogger(__name__)


def log_down(data: Dict[str, Any], rsu_esn: Optional[str] = None) -> None:
    LOG.info(f"log_down: rsu_esn={rsu_esn}, data={data}")
    topic = V2X_RSU_LOG_UP
    if rsu_esn is not None:
        topic = v2x_rsu_log_conf_down(rsu_esn)
    send_msg(topic, data)
