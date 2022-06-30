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
        engine = create_engine(CONF.database.connection, pool_pre_ping=True)

    global DB_SESSION_LOCAL
    DB_SESSION_LOCAL = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    LOG.info("DB setup complete")
