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

bind = ["0.0.0.0:28300"]
# bind = "unix://tmp/dandelion.sock"
workers = 1
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 300
keepalive = 5
reuse_port = True
proc_name = "dandelion"

logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "root": {"level": "DEBUG", "handlers": ["console"]},
    "loggers": {
        "gunicorn.error": {
            "level": "DEBUG",
            "handlers": ["error_file"],
            "propagate": 0,
            "qualname": "gunicorn_error",
        },
        "gunicorn.access": {
            "level": "DEBUG",
            "handlers": ["access_file"],
            "propagate": 0,
            "qualname": "access",
        },
    },
    "handlers": {
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "generic",
            "filename": "/var/log/dandelion/error.log",
        },
        "access_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "generic",
            "filename": "/var/log/dandelion/access.log",
        },
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "generic",
        },
    },
    "formatters": {
        "generic": {
            "format": "%(asctime)s.%(msecs)03d %(process)d %(levelname)s [-] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        }
    },
}
