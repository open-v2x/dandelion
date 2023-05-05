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

import json
from typing import Dict

from sqlalchemy.orm import Session
from starlette import status

from dandelion import crud, schemas
from dandelion.api.deps import OpenV2XHTTPException as HTTPException, get_redis_conn
from dandelion.models import MNG
from dandelion.models.mng import Reboot
from dandelion.util import ALGO_CONFIG


def get_mng_default() -> MNG:
    mng = MNG()
    mng.heartbeat_rate = 0
    mng.running_info_rate = 0
    mng.log_level = "NOLog"
    mng.reboot = Reboot.not_reboot
    mng.address_change = {"cssUrl": "", "time": 0}
    mng.extend_config = ""
    return mng


def pca_data_deal(data_all, code, next_=None):
    # 省市区数据结构
    data_: Dict = {}
    for i in data_all:
        key_code = i.__dict__.get(code)
        if key_code not in data_:
            data_[key_code] = []
        data = {"name": i.name, "code": i.code}
        if not next_:
            data_[key_code].append(data)
            continue
        if next_.get(i.code):
            data["children"] = next_.get(i.code, [])
            data_[key_code].append(data)

    return data_


def pca_data(db: Session):
    # 获取 省市区三级数据
    redis_conn = get_redis_conn()
    redis_data = redis_conn.get("PCD_DATA")
    if not redis_data:
        countries = crud.country.get_multi(db)
        provinces = crud.province.get_multi(db)
        citys = crud.city.get_multi_with_total(db)
        areas = crud.area.get_multi_with_total(db)
        area_ = pca_data_deal(areas, "city_code")
        city_ = pca_data_deal(citys, "province_code", area_)
        province_ = pca_data_deal(provinces, "country_code", city_)
        redis_data = json.dumps(
            [{**co.to_dict(), "children": province_.get(co.code, [])} for co in countries]
        )
        redis_conn.set("PCD_DATA", redis_data)

    return json.loads(redis_data)


def algo_module_name(db, algo_version_in, update=False):
    """"""
    module = algo_version_in.module
    algo = algo_version_in.algo
    module_in_db = crud.algo_module.get_by_name(db=db, module=module)
    if not module_in_db:
        module_in_db = crud.algo_module.create(
            db=db, obj_in=schemas.AlgoModuleCreate(module=module)
        )
    algo_name_in_db = crud.algo_name.get_by_name_and_module(
        db=db, algo=algo, module_id=module_in_db.id
    )
    in_use = (
        algo_version_in.in_use
        if algo_version_in.in_use is not None
        else ALGO_CONFIG.get(f"{module}_{algo}").get("inUse")
    )

    if (
        update
        and not crud.algo_version.get_by_version(db=db, version=in_use)
        and in_use != ALGO_CONFIG.get(f"{module}_{algo}").get("inUse")
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"version {in_use} does not exist"
        )
    if not algo_name_in_db:
        algo_name_in_db = crud.algo_name.create(
            db=db,
            obj_in=schemas.AlgoNameCreate(
                module_id=module_in_db.id,
                name=algo,
                enable=algo_version_in.enable
                if algo_version_in.enable is not None
                else ALGO_CONFIG.get(f"{module}_{algo}").get("enable"),
                in_use=algo_version_in.in_use
                if algo_version_in.in_use is not None
                else ALGO_CONFIG.get(f"{module}_{algo}").get("inUse"),
                module_path=algo_version_in.module_path
                if algo_version_in.module_path is not None
                else ALGO_CONFIG.get(f"{module}_{algo}").get("modulePath"),
            ),
        )
    return algo_name_in_db
