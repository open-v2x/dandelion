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

import urllib
from logging import LoggerAdapter
from typing import List

import redis
from oslo_config import cfg
from oslo_log import log
from oslo_utils import strutils
from redis import sentinel

CONF: cfg = cfg.CONF
LOG: LoggerAdapter = log.getLogger(__name__)

REDIS_CONN: redis.Redis

CLIENT_ARGS = frozenset(
    [
        "db",
        "encoding",
        "retry_on_timeout",
        "socket_keepalive",
        "socket_timeout",
        "ssl",
        "ssl_certfile",
        "ssl_keyfile",
        "sentinel",
        "sentinel_fallback",
    ]
)

CLIENT_BOOL_ARGS = frozenset(
    [
        "retry_on_timeout",
        "ssl",
    ]
)

CLIENT_LIST_ARGS = frozenset(
    [
        "sentinel_fallback",
    ]
)

CLIENT_INT_ARGS = frozenset(
    [
        "db",
        "socket_keepalive",
        "socket_timeout",
    ]
)

DEFAULT_SOCKET_TIMEOUT: int = 30


def setup_redis() -> None:
    parser_url, options_ = CONF.redis.connection.split("//", 1)[1].rsplit("?", 1)
    user_password, host_port = parser_url.rsplit("@", 1)
    user, password = user_password.split(":", 1)
    hostname, port = host_port.split(":")
    options = urllib.parse.parse_qs(options_)
    kwargs = {"host": hostname, "port": int(port), "password": password}

    for a in CLIENT_ARGS:
        if a not in options:
            continue
        if a in CLIENT_BOOL_ARGS:
            v = strutils.bool_from_string(options[a][0])
        elif a in CLIENT_LIST_ARGS:
            v = options[a]
        elif a in CLIENT_INT_ARGS:
            v = int(options[a][0])
        else:
            v = options[a]
        kwargs[a] = v
    if "socket_timeout" not in kwargs:
        kwargs["socket_timeout"] = DEFAULT_SOCKET_TIMEOUT

    # Ask the sentinel for the current master if there is a
    # sentinel arg.
    global REDIS_CONN
    if "sentinel" in kwargs:
        sentinel_hosts: List = [
            tuple(fallback.split(":")) for fallback in kwargs.get("sentinel_fallback", [])
        ]
        sentinel_hosts.insert(0, (kwargs["host"], kwargs["port"]))
        sentinel_server = sentinel.Sentinel(
            sentinel_hosts, socket_timeout=kwargs["socket_timeout"]
        )
        sentinel_name = kwargs["sentinel"][0]
        del kwargs["sentinel"]
        if "sentinel_fallback" in kwargs:
            del kwargs["sentinel_fallback"]
        REDIS_CONN = sentinel_server.master_for(sentinel_name, **kwargs)
    else:
        REDIS_CONN = redis.StrictRedis(**kwargs)
    LOG.info("Redis setup complete")
