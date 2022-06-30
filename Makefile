SHELL := /bin/bash

PYTHON ?= python3
SOURCES := dandelion
TOOLS := tools
ROOT_DIR ?= $(shell git rev-parse --show-toplevel)

# Color
no_color = \033[0m
black = \033[0;30m
red = \033[0;31m
green = \033[0;32m
yellow = \033[0;33m
blue = \033[0;34m
purple = \033[0;35m
cyan = \033[0;36m
white = \033[0;37m

# Version
RELEASE_VERSION ?= $(shell git rev-parse --short HEAD)_$(shell date -u +%Y-%m-%dT%H:%M:%S%z)
GIT_BRANCH ?= $(shell git rev-parse --abbrev-ref HEAD)
GIT_COMMIT ?= $(shell git rev-parse --verify HEAD)

# Database manage
REV_MEG ?=

.PHONY: all help venv install fmt lint server clean db_revision db_sync swagger config build future_check

all:
	make venv
	make fmt
	make lint
	make swagger
	make config
	make future_check

help:
	@echo "Dandelion development makefile"
	@echo
	@echo "Usage: make <TARGET>"
	@echo
	@echo "Target:"
	@echo "  venv                Create virtualenvs."
	@echo "  install             Installs the project dependencies."
	@echo "  fmt                 Code format."
	@echo "  lint                Code lint."
	@echo "  server              Run Server."
	@echo "  clean               Clean tmp resources."
	@echo "  db_revision         Generate database alembic version revision with model."
	@echo "  db_sync             Sync database from alembic version revision."
	@echo "  swagger             Generate swagger json file."
	@echo "  config              Generate sample config file."
	@echo "  build               Build docker image."
	@echo "  future_check        Find python files without 'type annotations'.(Alpha)"
	@echo

venv:
	tox -e venv

install:
	tox -e install
	source .tox/install/bin/activate && python setup.py install && deactivate

fmt:
	tox -e pep8-format

lint:
	tox -e pep8

server: install
	source .tox/install/bin/activate && uvicorn --reload --reload-dir dandelion --port 28300 --log-level debug dandelion.main:app --host 0.0.0.0

clean:
	rm -rf $(ROOT_DIR)/build
	rm -rf $(ROOT_DIR)/dist
	rm -rf $(ROOT_DIR)/.venv
	rm -rf $(ROOT_DIR)/test_report.html
	rm -rf $(ROOT_DIR)/.tox

db_revision:
	$(shell [ -z "$(REV_MEG)" ] && printf '$(red)Missing required message, use "make db_revision REV_MEG=<some message>"$(no_color)')
	source .tox/venv/bin/activate && alembic revision --autogenerate -m '$(REV_MEG)' && deactivate

db_sync:
	source .tox/venv/bin/activate && alembic upgrade head && deactivate

swagger:
	tox -e genswagger

config:
	tox -e genconfig

BUILD_ENGINE ?= docker
BUILD_CONTEXT ?= .
DOCKER_FILE ?= Dockerfile
IMAGE ?= dandelion
IMAGE_TAG ?= latest
ifeq ($(BUILD_ENGINE), docker)
    build_cmd = docker build
else ifeq ($(BUILD_ENGINE), buildah)
    build_cmd = buildah bud
else
    $(error Unsupported build engine $(BUILD_ENGINE))
endif
build:
	$(build_cmd) --no-cache --pull --force-rm --build-arg RELEASE_VERSION=$(RELEASE_VERSION) --build-arg GIT_BRANCH=$(GIT_BRANCH) --build-arg GIT_COMMIT=$(GIT_COMMIT) $(BUILD_ARGS) -f $(DOCKER_FILE) -t $(IMAGE):$(IMAGE_TAG) $(BUILD_CONTEXT)

# Find python files without "type annotations"
future_check:
	@find dandelion ! -size 0 -type f -name '*.py' -exec grep -L 'from __future__ import annotations' {} \;
