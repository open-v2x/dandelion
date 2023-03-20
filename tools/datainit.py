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
import datetime
import json
import os
import shutil
from pathlib import Path

from oslo_config import cfg
from sqlalchemy.orm import Session

from dandelion import conf, constants, version
from dandelion.core.security import get_password_hash
from dandelion.db import session as db_session
from dandelion.models import Area, City, Country, Map, Province, User

CONF: cfg = conf.CONF


def init_db() -> None:
    CONF(
        args=["--config-file", constants.CONFIG_FILE_PATH],
        project=constants.PROJECT_NAME,
        version=version.version_string(),
    )

    db_session.setup_db()
    session_: Session = db_session.DB_SESSION_LOCAL()

    user = User()
    user.username = "admin"
    user.hashed_password = get_password_hash("dandelion")
    user.is_active = 1
    user.is_superuser = 1
    session_.add(user)

    country1 = Country()
    country1.code = "CN"
    country1.name = "中国"
    session_.add(country1)
    session_.commit()

    base_path = Path(__file__).resolve().parent.parent
    with open(Path(base_path) / "pca.json") as f:
        pca_data = json.loads(f.read())
    p_, c_, a_ = [], [], []
    for p in pca_data:
        p_.append({"country_code": "CN", "name": p.get("name"), "code": p.get("code")})
        city_list = p.get("city_list")
        for c in city_list:
            c_.append(
                {"name": c.get("name"), "code": c.get("code"), "province_code": p.get("code")}
            )
            area_list = c.get("area_list")
            for a in area_list:
                a_.append(
                    {"name": a.get("name"), "code": a.get("code"), "city_code": c.get("code")}
                )
    session_.bulk_insert_mappings(Province, p_)
    session_.bulk_insert_mappings(City, c_)
    session_.bulk_insert_mappings(Area, a_)

    with open(Path(base_path) / "default_map.json") as f:
        data = json.loads(f.read())
    filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')}.jpg"
    if not os.path.exists(f"{constants.BITMAP_FILE_PATH}/{filename}"):
        shutil.copyfile(Path(base_path) / "map_bg.jpg", f"{constants.BITMAP_FILE_PATH}/{filename}")

    map = Map()
    map.name = "map"
    map.desc = "map"
    map.data = data
    map.bitmap_filename = filename
    session_.add(map)

    session_.commit()


init_db()
