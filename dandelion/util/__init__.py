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
