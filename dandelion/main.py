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

import time
import uuid
from logging import LoggerAdapter

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI, Request
from fastapi_utils.tasks import repeat_every
from oslo_config import cfg
from oslo_log import log
from pytz import utc
from starlette.middleware.cors import CORSMiddleware

from dandelion import constants, periodic_tasks, version
from dandelion.api.api_v1.api import api_router
from dandelion.db import redis_pool, session as db_session
from dandelion.mqtt import cloud_server as mqtt_cloud_server, server as mqtt_server

CONF: cfg = cfg.CONF
LOG: LoggerAdapter = log.getLogger(__name__)

app = FastAPI(
    title="Dandelion - OpenV2X Device Management - APIServer",
    openapi_url=f"{constants.API_V1_STR}/openapi.json",
)

role_conf = CONF.role


# Startup
@app.on_event("startup")
def prepare() -> None:
    log.register_options(CONF)
    CONF(
        args=["--config-file", constants.CONFIG_FILE_PATH],
        project=constants.PROJECT_NAME,
        version=version.version_string(),
    )
    log.setup(CONF, constants.PROJECT_NAME)


@app.on_event("startup")
def setup_mqtt() -> None:
    mqtt_server.connect()


@app.on_event("startup")
def setup_db() -> None:
    db_session.setup_db()


@app.on_event("startup")
def setup_cloud_mqtt() -> None:
    if "edge" == role_conf.run_role or "coexist" == role_conf.run_role:
        mqtt_cloud_server.connect()


@app.on_event("startup")
def setup_redis() -> None:
    redis_pool.setup_redis()


@app.on_event("startup")
def setup_app():
    # Set all CORS enabled origins
    if CONF.cors.origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=CONF.cors.origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )


@app.on_event("startup")
def setup_rsu_running():
    job_stores = {"default": MemoryJobStore()}
    executors = {"default": ThreadPoolExecutor(5)}
    job_defaults = {"coalesce": False, "max_instances": 3}
    scheduler = BackgroundScheduler(
        jobstores=job_stores, executors=executors, job_defaults=job_defaults, timezone=utc
    )
    scheduler.add_job(periodic_tasks.rsu_info, trigger="cron", minute="00,10,20,30,40,50")
    scheduler.start()


@app.on_event("startup")
@repeat_every(seconds=60)
def update_rsu_online_status() -> None:
    periodic_tasks.update_rsu_online_status()


@app.on_event("startup")
@repeat_every(seconds=60)
def delete_offline_edge() -> None:
    periodic_tasks.delete_offline_edge()


@app.on_event("startup")
@repeat_every(seconds=10)
def edge_heartbeat() -> None:
    periodic_tasks.edge_heartbeat()


# Shutdown
@app.on_event("shutdown")
def shutdown_event():
    LOG.info("Shutting down...")


# Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.middleware("http")
async def add_request_id_header(request: Request, call_next):
    request_id = uuid.uuid4().hex
    LOG.info(f"Request path: {request.url.path}, request id: {request_id}")
    response = await call_next(request)
    response.headers["OpenV2X-Request-ID"] = request_id
    return response


app.include_router(api_router, prefix=constants.API_V1_STR)
