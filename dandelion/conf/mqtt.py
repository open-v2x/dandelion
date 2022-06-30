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

from oslo_config import cfg

mqtt_group = cfg.OptGroup(
    name="mqtt",
    title="MQTT Options",
    help="""
MQTT related options.
""",
)

mqtt_opts = [
    cfg.IPOpt(
        "host",
        help="""
Host of MQTT server.
""",
    ),
    cfg.PortOpt(
        "port",
        default=1883,
        help="""
Port of MQTT server.
""",
    ),
    cfg.StrOpt(
        "username",
        help="""
Username of MQTT server.
""",
    ),
    cfg.StrOpt(
        "password",
        help="""
Password for username of MQTT server.
""",
    ),
]


def register_opts(conf):
    conf.register_group(mqtt_group)
    conf.register_opts(mqtt_opts, group=mqtt_group)


def list_opts():
    return {mqtt_group: mqtt_opts}
