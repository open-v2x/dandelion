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
from typing import Any, Dict, Generator, Optional

import requests
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


class OpenV2XHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        if detail.startswith("(sqlite3.IntegrityError)"):
            detail = {"code": 1062, "msg": detail.split(")")[1].split(":")[1].split(".")[1]}
        elif detail.startswith("(pymysql"):
            code, msg = eval(re.findall(r"\(.*?\)", detail)[1])
            detail = {"code": code, "msg": re.findall("'.*?'", msg)[0]}
        if not isinstance(detail, dict):
            detail = {"code": status_code, "msg": detail}
        super().__init__(status_code=status_code, detail=detail, headers=headers)


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
        raise OpenV2XHTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=err)
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        err = "User not found."
        LOG.error(err)
        raise OpenV2XHTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=err)
    return user


def get_token(host: str) -> str:
    login_url = f"http://{host}:28300/api/v1/login"
    login_res = requests.post(url=login_url, json={"username": "admin", "password": "dandelion"})
    res = login_res.json()
    return f"{res.get('token_type')} {res.get('access_token')}"
