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

from dandelion.conf import cors, database, mode, mqtt, redis, token

CONF: cfg = cfg.CONF


cors.register_opts(CONF)
database.register_opts(CONF)
mqtt.register_opts(CONF)
redis.register_opts(CONF)
token.register_opts(CONF)
mode.register_opts(CONF)
