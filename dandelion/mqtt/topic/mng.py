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


def v2x_rsu_mng_down(rsu_esn):
    return f"V2X/RSU/{rsu_esn}/MNG/DOWN"


def v2x_rsu_mng_down_ack(rsu_esn):
    return f"V2X/RSU/{rsu_esn}/MNG/DOWN/ACK"
