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

from datetime import timedelta
from logging import LoggerAdapter

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from oslo_config import cfg
from oslo_log import log
from sqlalchemy.orm import Session

from dandelion import conf, crud, schemas
from dandelion.api import deps
from dandelion.core import security

LOG: LoggerAdapter = log.getLogger(__name__)
CONF: cfg = conf.CONF

router = APIRouter()


class PasswordRequestForm(OAuth2PasswordRequestForm):
    def __init__(self, username: str = Body(...), password: str = Body(...)):
        super().__init__(
            grant_type="password",
            username=username,
            password=password,
            scope="",
            client_id=None,
            client_secret=None,
        )


@router.post(
    "",
    response_model=schemas.Token,
    status_code=status.HTTP_200_OK,
    summary="Login",
    description="""
User login with username and password.
""",
    responses={
        200: {"model": schemas.Token, "description": "OK"},
        400: {"model": schemas.ErrorMessage, "description": "Bad Request"},
    },
)
def login(
    db: Session = Depends(deps.get_db),
    form_data: PasswordRequestForm = Depends(),
) -> schemas.Token:
    """Login with the given password and username.

    :param db: db session, defaults to Depends(deps.get_db)
    :type db: Session, optional
    :param form_data: username and password, defaults to Depends()
    :type form_data: PasswordRequestForm, optional
    :raises HTTPException: 400
    :return: token
    :rtype: Token
    """
    LOG.debug(f"Login with username {form_data.username}.")
    user = crud.user.authenticate(db, username=form_data.username, password=form_data.password)
    if not user:
        err = "Incorrect username or password."
        LOG.error(err)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

    access_token_expires = timedelta(seconds=CONF.token.expire_seconds)
    access_token = security.create_access_token(user.id, expires_delta=access_token_expires)
    return schemas.Token(access_token=access_token, token_type="bearer")


@router.post(
    "/access-token",
    response_model=schemas.Token,
    summary="Login Access Token(DO NOT USE IN PRODUCTION)",
    description="""
- `DO NOT USE IN PRODUCTION !!!`
- `JUST FOR TESTING PURPOSE !!!`
""",
    responses={
        200: {"model": schemas.Token, "description": "OK"},
        400: {"model": schemas.ErrorMessage, "description": "Bad Request"},
    },
)
def access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> schemas.Token:
    """Creates a new access token.

    :param db: db session, defaults to Depends(deps.get_db)
    :type db: Session, optional
    :param form_data: form data, defaults to Depends()
    :type form_data: OAuth2PasswordRequestForm, optional
    :raises HTTPException: 400
    :return: token
    :rtype: Token
    """
    user = crud.user.authenticate(db, username=form_data.username, password=form_data.password)
    if not user:
        err = "Incorrect username or password."
        LOG.error(err)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=err)

    access_token_expires = timedelta(seconds=CONF.token.expire_seconds)
    access_token = security.create_access_token(user.id, expires_delta=access_token_expires)
    return schemas.Token(access_token=access_token, token_type="bearer")
