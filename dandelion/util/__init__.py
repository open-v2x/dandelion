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

import copy
import re
from typing import List

import yaml

from dandelion import constants
from dandelion.models import AlgoName


class Optional(object):  # noqa
    def __init__(self, val):
        self.val = val

    @staticmethod
    def none(val):
        return Optional(val)

    def map(self, func):
        if self.val is None:
            return self
        self.val = func(self.val)
        return self

    def get(self):
        return self.val

    def orElse(self, val_):
        if self.val is None:
            return val_
        return self.get()


def camel2underscore(name):
    """Camel to underscore

    >>> camel2underscore('testTESTTestTest0testTEST')
    'test_test_test_test0test_test'

    """

    name = name[0].upper() + name[1:]
    name = re.sub(r"([A-Z][a-z0-9]+)", r"_\1_", name).strip("_").lower()
    return re.sub(r"_+", "_", name)


def json_to_class(dict_, obj, hump=False):
    for v_ in dict_:
        key = v_
        if hump:
            key = camel2underscore(v_)
        obj.__setattr__(key, dict_.get(v_))
    return obj


def get_algo_config():
    algos = yaml.safe_load(constants.DEFAULT_ALGO)
    data = {}
    i = 1
    for module, algo_obj in algos.items():
        for algo_name, algo in algo_obj.get("algos").items():
            data[f"{module}_{algo_name}"] = {
                "id": i,
                "module": module,
                "algo": algo_name,
                "enable": algo.get("enable"),
                "modulePath": algo.get("module"),
                "inUse": algo.get("algo"),
                "version": [{"id": None, "version": v} for v in algo.get("version")],
            }
            i += 1
    return data


ALGO_CONFIG = get_algo_config()


def get_all_algo_config(data: List[AlgoName]):
    response_data = copy.deepcopy(ALGO_CONFIG)
    for algo_name_in_db in data:
        key = f"{algo_name_in_db.module}_{algo_name_in_db.name}"
        if response_data.get(key):
            response_data.get(key)["version"].extend(
                [v.to_dict() for v in algo_name_in_db.algo_versions]
            )
            response_data.get(key)["enable"] = algo_name_in_db.enable
            response_data.get(key)["inUse"] = algo_name_in_db.in_use
            response_data.get(key)["updateTime"] = algo_name_in_db.update_time
            version = {
                version.version: version.version_path for version in algo_name_in_db.algo_versions
            }
            if algo_name_in_db.in_use in version.keys():
                response_data.get(key)["modulePath"] = version.get(algo_name_in_db.in_use)
    return response_data
