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

# flake8: noqa: F401

from __future__ import annotations

# Import all the models, so that Base has them before being
# imported by Alembic
from dandelion.db.base_class import Base
from dandelion.models.area import Area
from dandelion.models.camera import Camera
from dandelion.models.city import City
from dandelion.models.country import Country
from dandelion.models.mng import MNG
from dandelion.models.province import Province
from dandelion.models.radar import Radar
from dandelion.models.rsi_event import RSIEvent
from dandelion.models.rsm import RSM
from dandelion.models.rsm_participants import Participants
from dandelion.models.rsu import RSU
from dandelion.models.rsu_config import RSUConfig
from dandelion.models.rsu_config_rsu import RSUConfigRSU
from dandelion.models.rsu_log import RSULog
from dandelion.models.rsu_model import RSUModel
from dandelion.models.rsu_query import RSUQuery
from dandelion.models.rsu_query_result import RSUQueryResult
from dandelion.models.rsu_query_result_data import RSUQueryResultData
from dandelion.models.rsu_tmp import RSUTMP
from dandelion.models.user import User
