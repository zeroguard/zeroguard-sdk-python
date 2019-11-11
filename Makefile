SHELL := bash
MAKEFLAGS += --warn-undefined-variables
.SHELLFLAGS := -euo pipefail -c
SUBMAKE_OPTS := -s
ENV_FILE=.env

###############################################################################
# Configurable constants block
###############################################################################
PACKAGE_NAME := zeroguard_sdk
PIPENV_CMD_RUN := pipenv run

SPHINX_SOURCE_DIR := ./docs
SPHINX_BUILD_DIR := $(SPHINX_SOURCE_DIR)/_build
SPHINX_CMD_BUILD := $(PIPENV_CMD_RUN) sphinx-build

DOCKER_PROJECT := zeroguard
DOCKER_IMAGE := zeroguard-sdk-python
DOCKER_VERSION := 0.0.1

DOCKER_TAG := $(DOCKER_PROJECT)/$(DOCKER_IMAGE):$(DOCKER_VERSION)
DOCKER_RUN_OPTS := -it --rm -v `pwd`:/app

###############################################################################
# Inferred constants block
###############################################################################
export $(shell test -f $(ENV_FILE) && sed 's/=.*//' $(ENV_FILE))
-include $(ENV_FILE)

###############################################################################
# Host targets
###############################################################################
.PHONY: all
all:
	$(MAKE) $(SUBMAKE_OPTS) dtest

.PHONY: dbuild
dbuild:
	docker build . -t $(DOCKER_TAG) -f Dockerfile

.PHONY: dtest
dtest: dbuild
	$(MAKE) $(SUBMAKE_OPTS) CMD='make test' internal-drun

.PHONY: ddocs
ddocs: dbuild
	$(MAKE) $(SUBMAKE_OPTS) CMD='make docs' internal-drun

.PHONY: dpypi
dpypi: dbuild
	$(MAKE) $(SUBMAKE_OPTS) CMD='make pypi' internal-drun

.PHONY: dshell
dshell: dbuild
	$(MAKE) $(SUBMAKE_OPTS) CMD='/bin/bash -i' internal-drun

.PHONY: dsafeshell
dsafeshell: dbuild
	$(MAKE) $(SUBMAKE_OPTS) CMD='--shell' internal-drun

.PHONY: dkill
dkill:
	docker kill $(DOCKER_TAG)

###############################################################################
# Guest targets
###############################################################################
.PHONY: init
init:
	pip3 install pipenv --upgrade
	pipenv install --dev

.PHONY: test
test:
	$(PIPENV_CMD_RUN) python3 -m pytest

.PHONY: docs
docs:
	$(SPHINX_CMD_BUILD) $(SPHINX_SOURCE_DIR) $(SPHINX_BUILD_DIR)

.PHONY: pypi
pypi:
	pip3 install 'twine>=1.5.0'
	python3 setup.py sdist bdist_wheel
	twine upload dist/* || :
	rm -rf build/ dist/ .egg $(PACKAGE_NAME).egg-info

###############################################################################
# Internal host targets
###############################################################################
.PHONY: internal-drun
internal-drun:
	docker run $(DOCKER_RUN_OPTS) $(DOCKER_TAG) $(CMD)

.PHONY: internal-dexec
internal-dexec:
	docker exec -it $(DOCKER_TAG) $(CMD)
