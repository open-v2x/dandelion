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

V2X_RSU_CONFIG_UP = "V2X/RSU/CONFIG/UP"
V2X_RSU_CONFIG_DOWN = "V2X/RSU/CONFIG/DOWN"
V2X_RSU_CONFIG_DOWN_ACK = "V2X/RSU/CONFIG/DOWN/ACK"
V2X_RSU_HB_UP = "V2X/RSU/HB/UP"
V2X_RSU_INFO_UP = "V2X/RSU/INFO/UP"


def v2x_rsu_config_up_ack(rsu_id):
    return f"V2X/RSU/{rsu_id}/CONFIG/UP/ACK"


def v2x_rsu_config_down(rsu_id):
    return f"V2X/RSU/{rsu_id}/CONFIG/DOWN"


def v2x_rsu_hb_up_ack(rsu_id):
    return f"V2X/RSU/{rsu_id}/HB/UP/ACK"


def v2x_rsu_info_up_ack(rsu_id):
    return f"V2X/RSU/{rsu_id}/INFO/UP/ACK"
