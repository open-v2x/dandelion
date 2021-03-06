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

database_group = cfg.OptGroup(
    name="database",
    title="Database Options",
    help="""
Database related options.
""",
)

database_opts = [
    cfg.StrOpt(
        "connection",
        default="sqlite:////tmp/dandelion.db",
        help="""
Connection of database.
""",
    ),
    cfg.IntOpt(
        "max_pool_size",
        default=50,
        help="""
Maximum number of SQL connections to keep open in a pool.
Setting a value of 0 indicates no limit.
""",
    ),
    cfg.IntOpt(
        "max_overflow",
        default=1000,
        help="""
If set, use this value for max_overflow with sqlalchemy.
""",
    ),
]


def register_opts(conf):
    conf.register_group(database_group)
    conf.register_opts(database_opts, group=database_group)


def list_opts():
    return {database_group: database_opts}
