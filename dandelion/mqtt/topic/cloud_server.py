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

V2X_EDGE_INFO_UP = "V2X/EDGE/INFO/UP"
V2X_EDGE_HB_UP = "V2X/EDGE/HB/UP"
V2X_EDGE_RSU_UP = "V2X/EDGE/RSU/UP"


def v2x_edge_key_info_up_ack(key):
    return f"V2X/EDGE/{key}/INFO/UP/ACK"
