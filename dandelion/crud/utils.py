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

from dandelion.models import MNG
from dandelion.models.mng import Reboot


def get_mng_default() -> MNG:
    mng = MNG()
    mng.heartbeat_rate = 0
    mng.running_info_rate = 0
    mng.log_level = "NOLog"
    mng.reboot = Reboot.not_reboot
    mng.address_change = {"cssUrl": "", "time": 0}
    mng.extend_config = ""
    return mng
