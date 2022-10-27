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

import re
from logging import LoggerAdapter
from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from oslo_config import cfg
from oslo_log import log
from pydantic import ValidationError
from redis import Redis
from sqlalchemy.orm import Session

from dandelion import conf, constants, crud, models, schemas
from dandelion.db import redis_pool, session

LOG: LoggerAdapter = log.getLogger(__name__)
CONF: cfg = conf.CONF

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{constants.API_V1_STR}/login/access-token")


def get_db() -> Generator:
    try:
        db: Session = session.DB_SESSION_LOCAL()
        yield db
    finally:
        db.close()


def get_redis_conn() -> Redis:
    return redis_pool.REDIS_CONN


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(token, CONF.token.secret_key, algorithms=[constants.ALGORITHM])
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        err = "Could not validate credentials."
        LOG.error(err)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"code": status.HTTP_403_FORBIDDEN, "msg": err},
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        err = "User not found."
        LOG.error(err)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": status.HTTP_404_NOT_FOUND, "msg": err},
        )
    return user


def error_msg_handle(err_msg: str) -> dict:
    code, msg = eval(re.findall(r"\(.*?\)", err_msg)[1])
    return {"code": code, "msg": re.findall("'.*?'", msg)[0]}
