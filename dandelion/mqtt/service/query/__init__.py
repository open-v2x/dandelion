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

import json
import time

from dandelion.mqtt import server
from dandelion.mqtt.topic.v2x_rsu import info_query


def down_query(
    rsu_id: str, rsu_esn: str, version: str, id: int, info_id: int, interval: int
) -> None:
    data = dict(
        rsuId=rsu_id,
        rsuEsn=rsu_esn,
        timestamp=int(time.time()),
        protocolVersion=version,
        infoId=info_id,
        interval=interval,
        ack=True,
        seqNum=f"{id}",
    )
    client = server.GET_MQTT_CLIENT()
    client.publish(topic=info_query(rsu_esn), payload=json.dumps(data), qos=0)
