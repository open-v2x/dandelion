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
from dandelion.models import (
    MNG,
    RSU,
    Area,
    City,
    Country,
    Intersection,
    Province,
    RSUConfig,
    RSUConfigRSU,
    SystemConfig,
    User,
)
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

    intersection1 = Intersection()
    intersection1.code = "32010601"
    intersection1.name = "鼓楼交叉路口"
    intersection1.lat = 31.9348466377
    intersection1.lng = 118.8213963998
    intersection1.area_code = "320106"
    session_.add(intersection1)

    intersection2 = Intersection()
    intersection2.code = "32011501"
    intersection2.name = "江宁交叉路口"
    intersection2.lat = 31.929900
    intersection2.lng = 118.862336
    intersection2.area_code = "320115"
    session_.add(intersection2)

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
    rsu1.rsu_status = "Normal"
    rsu1.online_status = False
    rsu1.location = {"lon": 118.8213963998, "lat": 31.9348466377}
    rsu1.config = {}
    rsu1.rsu_model_id = rsu_model1.id
    rsu1.intersection_code = "32011501"
    rsu1.desc = ""
    rsu1.bias_x = 0.0
    rsu1.bias_y = 0.0
    rsu1.rotation = 0.0
    rsu1.reverse = False
    rsu1.scale = 0.09
    rsu1.lane_info = {
        "1": -1,
        "2": 1,
        "3": 1,
        "4": -1,
        "5": -1,
        "6": -1,
        "7": -1,
        "8": 1,
        "9": 1,
        "10": 1,
        "11": 1,
        "12": 1,
        "13": 1,
        "14": -1,
        "15": -1,
        "16": 1,
        "17": 1,
        "18": 1,
        "19": 1,
        "20": -1,
        "21": -1,
        "22": -1,
        "23": -1,
        "24": -1,
    }

    mng1 = MNG()
    mng1.heartbeat_rate = 0
    mng1.running_info_rate = 0
    mng1.log_level = "NOLog"
    mng1.reboot = "not_reboot"
    mng1.address_change = dict(cssUrl="", time=0)
    mng1.extend_config = ""
    rsu1.mng = mng1
    session_.add(rsu1)

    rsu2 = RSU()
    rsu2.rsu_id = "8361"
    rsu2.rsu_esn = "R329329"
    rsu2.rsu_name = "RSU02"
    rsu2.rsu_ip = "192.168.0.103"
    rsu2.version = "v1"
    rsu2.rsu_status = "Normal"
    rsu2.online_status = False
    rsu2.location = {"lon": 118.862336, "lat": 31.929900}
    rsu2.config = {}
    rsu2.rsu_model_id = rsu_model1.id
    rsu2.intersection_code = "32011501"
    rsu2.desc = ""
    rsu2.bias_x = 74.67
    rsu2.bias_y = 78.91
    rsu2.rotation = 2.0
    rsu2.reverse = True
    rsu2.scale = 0.09
    rsu2.lane_info = {
        "1": -1,
        "2": 1,
        "3": 1,
        "4": -1,
        "5": -1,
        "6": -1,
        "7": -1,
        "8": 1,
        "9": 1,
        "10": 1,
        "11": 1,
        "12": 1,
        "13": 1,
        "14": -1,
        "15": -1,
        "16": 1,
        "17": 1,
        "18": 1,
        "19": 1,
        "20": -1,
        "21": -1,
        "22": -1,
        "23": -1,
        "24": -1,
    }

    mng2 = MNG()
    mng2.heartbeat_rate = 0
    mng2.running_info_rate = 0
    mng2.log_level = "NOLog"
    mng2.reboot = "not_reboot"
    mng2.address_change = dict(cssUrl="", time=0)
    mng2.extend_config = ""
    rsu2.mng = mng2
    session_.add(rsu2)

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

    system_config = SystemConfig()
    system_config.name = ""
    system_config.mqtt_config = None
    session_.add(system_config)

    session_.commit()


init_db()
