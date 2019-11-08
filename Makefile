SHELL := bash
MAKEFLAGS += --warn-undefined-variables
.SHELLFLAGS := -euo pipefail -c
SUBMAKE_OPTS := -s
ENV_FILE=.env

###############################################################################
# Configurable constants block
###############################################################################
PACKAGE_NAME := zeroguard
PIPENV_CMD_RUN := pipenv run

###############################################################################
# Inferred constants block
###############################################################################
export $(shell test -f $(ENV_FILE) && sed 's/=.*//' $(ENV_FILE))
-include $(ENV_FILE)

.PHONY: all
all:

###############################################################################
# Host targets
###############################################################################
.PHONY: init
init:
	pip3 install pipenv --upgrade
	pipenv install --dev

.PHONY: publish
publish: init
	$(PIPENV_CMD_RUN) python setup.py sdist bdist_wheel
	$(PIPENV_CMD_RUN) twine upload dist/* || :
	rm -rf build/ dist/ .egg $(PACKAGE_NAME).egg-info
