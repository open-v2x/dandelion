#!/usr/bin/env bash
#
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

set -ex

echo "/usr/local/bin/gunicorn -c /etc/dandelion/gunicorn.py dandelion.main:app" >/run_command

mapfile -t CMD < <(tail /run_command | xargs -n 1)

if [[ "${!KOLLA_BOOTSTRAP[*]}" ]]; then
    cd /dandelion/
    alembic upgrade head
    python /dandelion/tools/datainit.py
    exit 0
fi

echo "Running command: ${CMD[*]}"
exec "${CMD[@]}"
