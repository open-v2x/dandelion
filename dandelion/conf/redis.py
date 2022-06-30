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

redis_group = cfg.OptGroup(
    name="redis",
    title="Redis Options",
    help="""
Redis related options.
""",
)

redis_opts = [
    cfg.StrOpt(
        "connection",
        help="""
Connection of redis.
If you have a single redis server, you can set connection as followed:
"redis://<user>:<password>@<ip>:<port>?db=0&socket_timeout=60&retry_on_timeout=yes".
If you have a sentinel redis cluster, you can set connection as followed:
"redis://<user>:<password>@<ip>:<port>?sentinel=<sentinel>&sentinel_fallback=<ip>:<port>&sentinel_fallback=<ip>:<port>&db=0&socket_timeout=60&retry_on_timeout=yes"
""",
    ),
]


def register_opts(conf):
    conf.register_group(redis_group)
    conf.register_opts(redis_opts, group=redis_group)


def list_opts():
    return {redis_group: redis_opts}
