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

from fastapi import APIRouter

from dandelion.api.api_v1.endpoints import (
    algos,
    areas,
    cameras,
    cgw,
    cities,
    cloud_homes,
    countries,
    edge_nodes,
    edge_site,
    lidars,
    login,
    map_rsus,
    maps,
    mngs,
    osw,
    provinces,
    radars,
    rdw,
    rsi_clcs,
    rsi_cwms,
    rsi_dnps,
    rsi_events,
    rsi_sdss,
    rsm_participants,
    rsu_configs,
    rsu_logs,
    rsu_models,
    rsu_queries,
    rsu_tmps,
    rsus,
    services,
    spats,
    ssw,
    system_configs,
    users,
)

api_router = APIRouter()

api_router.include_router(login.router, prefix="/login", tags=["User"])
api_router.include_router(users.router, prefix="/users", tags=["User"])

api_router.include_router(countries.router, prefix="/countries", tags=["Area"])
api_router.include_router(provinces.router, prefix="/provinces", tags=["Area"])
api_router.include_router(cities.router, prefix="/cities", tags=["Area"])
api_router.include_router(areas.router, prefix="/areas", tags=["Area"])

api_router.include_router(cameras.router, prefix="/cameras", tags=["Camera"])

api_router.include_router(cloud_homes.router, prefix="/homes", tags=["Cloud Control Home"])

api_router.include_router(mngs.router, prefix="/mngs", tags=["MNG"])
api_router.include_router(map_rsus.router, prefix="/maps", tags=["Map"])
api_router.include_router(maps.router, prefix="/maps", tags=["Map"])
api_router.include_router(radars.router, prefix="/radars", tags=["Radar"])
api_router.include_router(spats.router, prefix="/spats", tags=["Spat"])

api_router.include_router(lidars.router, prefix="/lidars", tags=["Lidar"])

api_router.include_router(rsi_events.router, prefix="/events", tags=["Event"])

api_router.include_router(rsm_participants.router, prefix="/rsms", tags=["RSM"])

api_router.include_router(rsu_configs.router, prefix="/rsu_configs", tags=["RSU Config"])

api_router.include_router(rsu_logs.router, prefix="/rsu_logs", tags=["RSU Log"])

api_router.include_router(rsu_models.router, prefix="/rsu_models", tags=["RSU Model"])

api_router.include_router(rsu_queries.router, prefix="/rsu_queries", tags=["RSU Query"])

api_router.include_router(rsu_tmps.router, prefix="/rsu_tmps", tags=["RSU TMP"])

api_router.include_router(rsus.router, prefix="/rsus", tags=["RSU"])

api_router.include_router(system_configs.router, prefix="/system_configs", tags=["System Config"])

api_router.include_router(rsi_dnps.router, prefix="/rsi_dnps", tags=["RSI DNP"])

api_router.include_router(rsi_cwms.router, prefix="/rsi_cwms", tags=["RSI CWM"])

api_router.include_router(rsi_clcs.router, prefix="/rsi_clcs", tags=["RSI CLC"])

api_router.include_router(rsi_sdss.router, prefix="/rsi_sdss", tags=["RSI SDS"])
api_router.include_router(cgw.router, prefix="/cgw", tags=["CGW"])
api_router.include_router(rdw.router, prefix="/rdw", tags=["RDW"])
api_router.include_router(osw.router, prefix="/osw", tags=["OSW"])
api_router.include_router(ssw.router, prefix="/ssw", tags=["SSW"])
api_router.include_router(edge_site.router, prefix="/edge_site", tags=["Edge Site"])
api_router.include_router(edge_nodes.router, prefix="/edge_nodes", tags=["Edge Node"])

api_router.include_router(algos.router, prefix="/algos", tags=["Algo"])

api_router.include_router(services.router, prefix="/service_types", tags=["Service"])
