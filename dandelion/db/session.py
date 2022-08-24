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

from logging import LoggerAdapter
from typing import Dict
from urllib.parse import quote_plus

from oslo_config import cfg
from oslo_log import log
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

CONF = cfg.CONF
LOG: LoggerAdapter = log.getLogger(__name__)

DB_SESSION_LOCAL: Session


def setup_db() -> None:
    if CONF.database.connection.startswith("sqlite"):
        engine = create_engine(
            CONF.database.connection,
            pool_pre_ping=True,
            connect_args={"check_same_thread": False},
        )
    else:
        engine_cfg: Dict[str, int] = {}
        engine_cfg["pool_size"] = CONF.database.max_pool_size
        engine_cfg["max_overflow"] = CONF.database.max_overflow

        connection = connection_database()

        engine = create_engine(connection, pool_pre_ping=True, **engine_cfg)

    global DB_SESSION_LOCAL
    DB_SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    LOG.info("DB setup complete")


def connection_database() -> str:
    connection_list = CONF.database.connection.split(":")
    index = connection_list[2].rfind("@")
    connection_list[2] = quote_plus(connection_list[2][:index]) + connection_list[2][index:]
    connection = ":".join(connection_list)
    return connection
