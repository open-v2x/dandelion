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
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Query, Response, status
from oslo_log import log
from sqlalchemy.orm import Session

from dandelion import crud, models, schemas
from dandelion.api import deps
from dandelion.api.deps import OpenV2XHTTPException as HTTPException
from dandelion.mqtt.service.rsu.rsu_algo import algo_publish
from dandelion.util import ALGO_CONFIG, get_all_algo_config

router = APIRouter()
LOG: LoggerAdapter = log.getLogger(__name__)


@router.post(
    "/version",
    response_model=schemas.AlgoVersion,
    status_code=status.HTTP_201_CREATED,
    description="""
Create a new version.
""",
    responses={
        status.HTTP_201_CREATED: {"model": schemas.AlgoVersion, "description": "Created"},
        status.HTTP_400_BAD_REQUEST: {"model": schemas.ErrorMessage, "description": "Bad Request"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def create(
    algo_version_in: schemas.AlgoVersionCreateAll,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.AlgoVersion:
    module = algo_version_in.module
    if not crud.algo_module.get_by_name(db=db, module=module):
        crud.algo_module.create(db=db, obj_in=schemas.AlgoModuleCreate(module=module))
    algo = algo_version_in.algo
    if not crud.algo_name.get_by_name_and_module(db=db, algo=algo, module=module):
        crud.algo_name.create(
            db=db,
            obj_in=schemas.AlgoNameCreate(
                module=module,
                name=algo,
                enable=algo_version_in.enable
                if algo_version_in.enable
                else ALGO_CONFIG.get(f"{module}_{algo}").get("enable"),
                in_use=algo_version_in.in_use
                if algo_version_in.in_use
                else ALGO_CONFIG.get(f"{module}_{algo}").get("inUse"),
                module_path=algo_version_in.module_path
                if algo_version_in.module_path
                else ALGO_CONFIG.get(f"{module}_{algo}").get("modulePath"),
            ),
        )

    new_algo_version_in_db = crud.algo_version.create(
        db,
        obj_in=schemas.AlgoVersionCreate(
            algo=algo, version=algo_version_in.version, version_path=algo_version_in.version_path
        ),
    )
    return new_algo_version_in_db.to_all_dict()


@router.delete(
    "/version/{version_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="""
Delete a version.
""",
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
    response_class=Response,
    response_description="No Content",
)
def delete(
    version_id: int,
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> Response:
    algo_version_db = crud.algo_version.get(db, id=version_id)
    if not algo_version_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Version [id: {version_id}] not found"
        )
    if algo_version_db.algo_name.in_use == algo_version_db.version:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"Version [id: {version_id}] is in use"
        )
    crud.algo_version.remove(db, id=version_id)
    return Response(content=None, status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "",
    response_model=schemas.AlgoNames,
    status_code=status.HTTP_200_OK,
    summary="List Algo",
    description="""
Search algo by name.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.AlgoNames, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get_all(
    algo: Optional[str] = Query(None, description="Filter by algo name", alias="algo"),
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.AlgoNames:
    total, data = crud.algo_name.get_multi_by_algo_name(db, algo=algo)
    response_data = get_all_algo_config(data=data)
    data_list = (
        list(response_data.values())
        if not algo
        else [value for value in response_data.values() if value.get("algo").find(algo) != -1]
    )
    return schemas.AlgoNames(total=len(data_list), data=data_list)


@router.get(
    "/version",
    response_model=schemas.AlgoVersions,
    status_code=status.HTTP_200_OK,
    summary="List version",
    description="""
Search version by name.
""",
    responses={
        status.HTTP_200_OK: {"model": schemas.AlgoVersions, "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get_all_version(
    version: Optional[str] = Query(None, description="Filter by algo version", alias="version"),
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> schemas.AlgoVersions:
    total, data = crud.algo_version.get_multi_by_version(db, version=version)
    data_list = [obj_in.to_all_dict() for obj_in in data]
    default_data = ALGO_CONFIG.values()
    for default_obj in default_data:
        for default_version in default_obj.get("version"):
            if not version or default_version.find(version) != -1:
                data_list.append(
                    {
                        "module": default_obj.get("module"),
                        "algo": default_obj.get("algo"),
                        "version": default_version,
                    }
                )
    data_list.sort(key=lambda x: (x.get("module"), x.get("algo")))
    return schemas.AlgoVersions(total=len(data_list), data=data_list)


@router.post(
    "",
    response_model=List[schemas.AlgoNameEdit],
    status_code=status.HTTP_200_OK,
    description="""
update algos.
""",
    responses={
        status.HTTP_200_OK: {"model": List[schemas.AlgoNameEdit], "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def update(
    algo_in: List[schemas.AlgoNameUpdateAll],
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> List[schemas.AlgoNameEdit]:
    default_algo = ALGO_CONFIG
    response_data = []
    for algo_obj in algo_in:
        module = algo_obj.module
        if not crud.algo_module.get_by_name(db=db, module=module):
            crud.algo_module.create(db=db, obj_in=schemas.AlgoModuleCreate(module=module))
        algo = algo_obj.algo
        algo_in_db = crud.algo_name.get_by_name_and_module(db=db, algo=algo, module=module)
        if not algo_in_db:
            new_algo_in_db = crud.algo_name.create(
                db=db,
                obj_in=schemas.AlgoNameCreate(
                    module=module,
                    name=algo,
                    enable=algo_obj.enable
                    if algo_obj.enable
                    else default_algo.get(f"{module}_{algo}").get("enable"),
                    in_use=algo_obj.in_use
                    if algo_obj.in_use
                    else default_algo.get(f"{module}_{algo}").get("inUse"),
                    module_path=default_algo.get(f"{module}_{algo}").get("modulePath"),
                ),
            )
        else:
            new_algo_in_db = crud.algo_name.update(
                db=db,
                db_obj=algo_in_db,
                obj_in=schemas.AlgoNameUpdate(**algo_obj.dict(exclude_unset=True)),
            )
        response_data.append(new_algo_in_db.to_dict())
    algo_publish(db=db)
    return response_data


@router.get(
    "/module",
    response_model=List[Dict[str, Any]],
    status_code=status.HTTP_200_OK,
    summary="List module algo",
    description="""
Get module algo.
""",
    responses={
        status.HTTP_200_OK: {"model": List[Dict[str, Any]], "description": "OK"},
        status.HTTP_401_UNAUTHORIZED: {
            "model": schemas.ErrorMessage,
            "description": "Unauthorized",
        },
        status.HTTP_403_FORBIDDEN: {"model": schemas.ErrorMessage, "description": "Forbidden"},
        status.HTTP_404_NOT_FOUND: {"model": schemas.ErrorMessage, "description": "Not Found"},
    },
)
def get_all_module_algo(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_user),
) -> List[Dict[str, Any]]:
    data = crud.algo_module.get_all(db)
    response_data = {}
    for default_algo in ALGO_CONFIG.values():
        if default_algo.get("module") not in response_data:
            response_data[default_algo.get("module")] = {
                "module": default_algo.get("module"),
                "algo": [],
            }
        response_data[default_algo.get("module")]["algo"].append(default_algo.get("algo"))
    for algo_in_db in data:
        response_data[algo_in_db.module]["algo"].extend(
            [algo.name for algo in algo_in_db.algo_name]
        )

    return [value for value in response_data.values()]
