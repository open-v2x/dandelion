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

token_group = cfg.OptGroup(
    name="token",
    title="Token Options",
    help="""
Token related options.
""",
)

token_opts = [
    cfg.IntOpt(
        "expire_seconds",
        default=604800,
        help="""
Token expire seonds. Default: 604800(7 days).
""",
    ),
    cfg.StrOpt(
        "secret_key",
        default="CP7l45i1SEk7jues8DAcO3MnWe-NMKITz3XrMxHBZhY",
        help="""
Secret key of token.
""",
    ),
]


def register_opts(conf):
    conf.register_group(token_group)
    conf.register_opts(token_opts, group=token_group)


def list_opts():
    return {token_group: token_opts}
