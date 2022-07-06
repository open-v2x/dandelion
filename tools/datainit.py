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

from oslo_config import cfg
from sqlalchemy.orm import Session

from dandelion import conf, constants, version
from dandelion.core.security import get_password_hash
from dandelion.db import session as db_session
from dandelion.models import MNG, RSU, Area, City, Country, Province, RSUConfig, RSUConfigRSU, User
from dandelion.models.rsu_model import RSUModel

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

    province2 = Province()
    province2.country_code = "CN"
    province2.code = "320000"
    province2.name = "江苏省"
    session_.add(province2)

    city1 = City()
    city1.province_code = "320000"
    city1.code = "320100"
    city1.name = "南京市"
    session_.add(city1)

    city2 = City()
    city2.province_code = "320000"
    city2.code = "320200"
    city2.name = "无锡市"
    session_.add(city2)

    area1 = Area()
    area1.city_code = "320100"
    area1.code = "320115"
    area1.name = "江宁区"
    session_.add(area1)

    area2 = Area()
    area2.city_code = "320100"
    area2.code = "320106"
    area2.name = "鼓楼区"
    session_.add(area2)

    area3 = Area()
    area3.city_code = "320200"
    area3.code = "320211"
    area3.name = "滨湖区"
    session_.add(area3)

    rsu_model1 = RSUModel()
    rsu_model1.name = "RSU1"
    rsu_model1.manufacturer = "华为"
    rsu_model1.desc = "RSU1的描述"
    session_.add(rsu_model1)
    session_.commit()
    session_.refresh(rsu_model1)

    rsu1 = RSU()
    rsu1.rsu_id = "45348"
    rsu1.rsu_esn = "R328328"
    rsu1.rsu_name = "RSU01"
    rsu1.rsu_ip = "192.168.0.102"
    rsu1.version = "v1"
    rsu1.rsu_status = "正常"
    rsu1.online_status = False
    rsu1.location = {}
    rsu1.config = {}
    rsu1.rsu_model_id = rsu_model1.id
    rsu1.area_code = "320115"
    rsu1.address = "江宁交叉路口"
    rsu1.desc = ""

    mng = MNG()
    mng.heartbeat_rate = 0
    mng.running_info_rate = 0
    mng.log_level = "NOLog"
    mng.reboot = "not_reboot"
    mng.address_change = dict(cssUrl="", time=0)
    mng.extend_config = ""
    rsu1.mng = mng
    session_.add(rsu1)

    config1 = RSUConfig()
    config1.name = "测试01"
    config1.bsm = {}
    config1.rsi = {}
    config1.rsm = {}
    config1.map = {}
    config1.spat = {}
    session_.add(config1)

    config_rsu1 = RSUConfigRSU()
    config_rsu1.rsu = rsu1
    config_rsu1.rsu_config = config1
    session_.add(config_rsu1)

    session_.commit()


init_db()
