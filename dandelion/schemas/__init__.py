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

from .area import Area, AreaCreate, AreaUpdate
from .camera import Camera, CameraCreate, Cameras, CameraUpdate
from .city import City, CityCreate, CityUpdate
from .cloud_home import OnlineRate, RouteInfo, RouteInfoCreate
from .country import Country, CountryCreate, CountryUpdate
from .edge_node import EdgeNodeCreate, EdgeNodes, EdgeNodeUpdate
from .edge_node_rsu import EdgeNodeRSUCreate, EdgeNodeRSUs, EdgeNodeRSUUpdate, Location
from .map import Map, MapCreate, Maps, MapUpdate
from .map_rsu import MapRSU, MapRSUCreate, MapRSUs, MapRSUUpdate
from .message import ErrorMessage, Message
from .mng import MNG, MNGCopy, MNGCreate, MNGs, MNGUpdate
from .province import Province, ProvinceCreate, ProvinceUpdate
from .radar import Radar, RadarCreate, Radars, RadarUpdate
from .rsi_dnp import RSIDNPCreate, RSIDNPs
from .rsi_event import RSIEvent, RSIEventCreate, RSIEvents, RSIEventUpdate
from .rsm import RSM, RSMCreate, RSMs, RSMUpdate
from .rsm_participant import (
    RSMParticipant,
    RSMParticipantCreate,
    RSMParticipants,
    RSMParticipantUpdate,
)
from .rsu import (
    RSU,
    RSUCreate,
    RSUDetail,
    RSULocation,
    RSUs,
    RSUUpdate,
    RSUUpdateWithStatus,
    RSUUpdateWithVersion,
)
from .rsu_config import RSUConfig, RSUConfigCreate, RSUConfigs, RSUConfigUpdate, RSUConfigWithRSUs
from .rsu_config_rsu import RSUConfigRSU, RSUConfigRSUCreate, RSUConfigRSUs, RSUConfigRSUUpdate
from .rsu_log import RSULog, RSULogCreate, RSULogs, RSULogUpdate
from .rsu_model import RSUModel, RSUModelCreate, RSUModels, RSUModelUpdate
from .rsu_query import RSUQueries, RSUQuery, RSUQueryCreate, RSUQueryDetail, RSUQueryUpdate
from .rsu_query_result import (
    RSUQueryResult,
    RSUQueryResultCreate,
    RSUQueryResults,
    RSUQueryResultUpdate,
)
from .rsu_tmp import RSUTMP, RSUTMPCreate, RSUTMPs, RSUTMPUpdate
from .system_config import MQTTConfig, SystemConfig, SystemConfigCreate
from .token import AccessToken, Token, TokenPayload
from .user import User, UserCreate, UserUpdate
