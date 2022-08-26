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

role_group = cfg.OptGroup(
    name="role",
    title="Run Role Options",
    help="""
Run Role related options.
""",
)

role_opts = [
    cfg.StrOpt(
        "run_role",
        default="coexist",
        help="""
Run role. Default: coexist
Possible values:
edge - The edge node sends data to the cloud control center
center - The cloud control center displays the data reported by the connected edge nodes
coexist - Coexistence of cloud control center and edge nodes
""",
    ),
]


def register_opts(conf):
    conf.register_group(role_group)
    conf.register_opts(role_opts, group=role_group)


def list_opts():
    return {role_group: role_opts}
