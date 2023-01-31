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

PROJECT_NAME: str = "dandelion"
CONFIG_FILE_PATH: str = "/etc/dandelion/dandelion.conf"
API_V1_STR: str = "/api/v1"
ALGORITHM: str = "HS256"
HTTP_REPEAT_CODE: int = 499
BITMAP_FILE_PATH: str = "/openv2x/data/bitmap"
DEFAULT_ALGO: str = """
rsi_formatter:
  algos:
    rsi_formatter:
      enable: true
      module: "transform_driver.rsi_service"
      algo: "rsi"
      version:
      - rsi
pre_process_ai_algo:
  algos:
    complement:
      enable: true
      module: "pre_process_ai_algo.algo_lib.complement"
      algo: "interpolation"
      version: 
      - interpolation
      - lstm_predict
    fusion:
      enable: false
      module: "pre_process_ai_algo.algo_lib.fusion"
      algo: "fusion"
      version:
      - fusion
    smooth:
      enable: true
      module: "pre_process_ai_algo.algo_lib.smooth"
      algo: "exponential"
      version:
      - exponential
      - polynomial
    visual:
      enable: true
      module: "pre_process_ai_algo.pipelines.visualization"
      algo: "visual"
      version:
      - visual
scenario_algo:
  algos:
    collision_warning:
      enable: true
      module: "scenario_algo.algo_lib.collision_warning"
      algo: "collision_warning"
      version:
      - collision_warning
    cooperative_lane_change:
      enable: true
      module: "scenario_algo.algo_lib.cooperative_lane_change"
      algo: "cooperative_lane_change"
      version:
      - cooperative_lane_change
    do_not_pass_warning:
      enable: true
      module: "scenario_algo.algo_lib.do_not_pass_warning"
      algo: "do_not_pass_warning"
      version:
      - do_not_pass_warning
    sensor_data_sharing:
      enable: true
      module: "scenario_algo.algo_lib.sensor_data_sharing"
      algo: "sensor_data_sharing"
      version:
      - sensor_data_sharing
post_process_algo:
  algos:
    post_process:
      enable: true
      module: "post_process_algo.post_process"
      algo: "post_process"
      version:
      - post_process
"""  # noqa: W291
