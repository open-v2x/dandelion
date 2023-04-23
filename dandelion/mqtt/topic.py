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

# map
V2X_RSU_MAP_DOWN = "V2X/RSU/MAP/DOWN"
# config
V2X_RSU_CONFIG_UP = "V2X/RSU/CONFIG/UP"
V2X_RSU_CONFIG_DOWN = "V2X/RSU/CONFIG/DOWN"
# log
V2X_RSU_LOG_UP = "V2X/RSU/Log/UP"
# server
V2X_RSU_HB_UP = "V2X/RSU/HB/UP"
V2X_RSU_INFO_UP = "V2X/RSU/INFO/UP"
# server
V2X_RSU_BaseINFO_UP = "V2X/RSU/BaseINFO/UP"
V2X_RSU_RunningInfo_UP = "V2X/RSU/RunningInfo/UP"
V2X_RSU_INFOQuery_Response = "V2X/RSU/INFOQuery/Response"
V2X_RSU_PLUS_CONFIG_DOWN_ACK = "V2X/RSU/+/CONFIG/DOWN/ACK"
V2X_RSU_PLUS_MAP_DOWN_ACK = "V2X/RSU/+/MAP/DOWN/ACK"
V2X_RSU_PLUS_MAP_UP = "V2X/RSU/+/MAP/UP"
V2X_RSU_PLUS_RSM_DOWN = "V2X/RSU/+/RSM/DOWN"
V2X_RSU_PLUS_RSI_DOWN = "V2X/RSU/+/RSI/DOWN"
V2X_RSU_PLUS_DNP_DOWN = "V2X/RSU/+/DNP/DOWN"
V2X_RSU_PLUS_CWM_DOWN = "V2X/RSU/+/CWM/DOWN"
V2X_RSU_PLUS_CLC_DOWN = "V2X/RSU/+/CLC/DOWN"
V2X_RSU_PLUS_SDS_DOWN = "V2X/RSU/+/SDS/DOWN"
V2X_RSU_PLUS_CGW_DOWN = "V2X/RSU/+/CGW/DOWN"
V2X_RSU_PLUS_RDW_DOWN = "V2X/RSU/+/RDW/DOWN"
RSU_SPAT_DOWN = "RSU/SPAT/DOWN"
V2X_RSU_PLUS_SPAT_UP = "V2X/RSU/+/SPAT/UP"
V2X_RSU_PLUS_OSW_DOWN = "V2X/RSU/+/OSW/DOWN"
V2X_RSU_PLUS_SSW_DOWN = "V2X/RSU/+/SSW/DOWN"
V2X_RSU_PIP_CFG = "V2X/RSU/PIP/CFG"

V2X_EDGE_SITE_CHANGE = "V2X/EDGE/SITE/CHANGE"


def v2x_rsu_map_down(rsu_id):
    return f"V2X/RSU/{rsu_id}/MAP/DOWN"


def v2x_rsu_mng_down(rsu_esn):
    return f"V2X/RSU/{rsu_esn}/MNG/DOWN"


def info_query(esn):
    return f"V2X/RSU/{esn}/INFOQuery"


def v2x_rsu_config_down(rsu_id):
    return f"V2X/RSU/{rsu_id}/CONFIG/DOWN"


def v2x_rsu_log_conf_down(rsu_esn):
    return f"V2X/RSU/{rsu_esn}/Log/UP"
