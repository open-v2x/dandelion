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

import importlib.util
import os
import re
from importlib._bootstrap import ModuleSpec
from logging import LoggerAdapter
from typing import Any, Dict, Generator, Optional, Union

import requests
import sqlalchemy.exc
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

RESPONSE_ERROR: Dict = {
    status.HTTP_400_BAD_REQUEST: {"model": schemas.ErrorMessage, "description": "Bad Request"},
    status.HTTP_401_UNAUTHORIZED: {
        "model": schemas.ErrorMessage,
        "description": "Unauthorized",
    },
    status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
    status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
}


class OpenV2XHTTPException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        if isinstance(detail, str) and detail.startswith("(pymysql.err.DataError)"):
            code, msg = eval(re.findall(r"\(pymysql.err.DataError\) (.*)", detail)[0])
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


def check_token(db, token):
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


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        return check_token(db=db, token=token)
    except OpenV2XHTTPException as e:
        error = e
    system_config = crud.system_config.get(db=db, id=1)
    if not system_config:
        raise error
    res = requests.get(
        url=os.path.join(
            system_config.center_dandelion_endpoint,
            constants.API_V1_STR.strip("/"),
            "login/check_token",
        ),
        headers={"token": token},
    )
    if res.status_code != status.HTTP_200_OK:
        raise error
    return res.json()


def get_current_user_no_auth(db: Session = Depends(get_db), token: str = "") -> models.User:
    return crud.user.get(db, id=1) or models.User()


if os.getenv("OPENV2X_DANDELION_NO_AUTH", "") == "true":
    get_current_user = get_current_user_no_auth  # noqa F811


def get_token(host: str) -> str:
    login_url = f"http://{host}:28300/api/v1/login"
    login_res = requests.post(
        url=login_url, json={"username": CONF.user.username, "password": CONF.user.password}
    )
    res = login_res.json()
    return f"{res.get('token_type')} {res.get('access_token')}"


def error_handle(
    err: sqlalchemy.exc.DatabaseError,
    field: Union[str, list],
    field_data: Union[str, list, None] = None,
):
    err_msg = err.args[0]
    LOG.error(err_msg)
    if isinstance(err, sqlalchemy.exc.IntegrityError):
        code = err.orig.args[0]
        detail = {
            "code": code,
            "msg": err_msg,
            "detail": {},
        }
        if code == 1062:  # 重复
            if isinstance(field, list) and isinstance(field_data, list):
                for index, value in enumerate(field):
                    detail["detail"][value] = field_data[index]
            else:
                detail["detail"][field] = field_data
        return OpenV2XHTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )
    return OpenV2XHTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err_msg)


def crud_get(db, obj_id, crud_model, detail):
    data = crud_model.get(db, id=obj_id)
    if not data:
        raise OpenV2XHTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{detail}  [id: {obj_id}] not found",
        )
    return data


def get_gunicorn_port():
    spec: ModuleSpec = importlib.util.spec_from_file_location(
        "gunicorn_config", "/etc/dandelion/gunicorn.py"
    )
    try:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        bind_str = module.bind[0]
        port = bind_str.split(":")[-1]
        return port
    except (AttributeError, ImportError, IndexError, ValueError):
        return "28300"


def spat_intersection_phase_unique(
    ex: sqlalchemy.exc.DatabaseError, spat_in: Union[schemas.SpatCreate, schemas.SpatUpdate]
):
    match = re.search(r"Duplicate entry '.*' for key '(.*?)'", ex.orig.args[1])
    if match and match.group(1) != "ix_spat_name":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "code": 1063,
                "msg": ex.args[0],
                "detail": {
                    "intersection_id": spat_in.intersection_id,
                    "phase_id": spat_in.phase_id,
                },
            },
        )
    else:
        raise error_handle(ex, "name", spat_in.name)
