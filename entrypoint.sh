#!/usr/bin/env bash
#
###############################################################################
# Title:       entrypoint.dev
# Description: Install Pipenv dependencies and run a passed in command
# Usage:       Specify as Docker entrypoint and pass a command to execute when
#              running 'docker run' (command may span multiple arguments)
###############################################################################
set -euo pipefail

readonly LOG_PREF_INFO='---(i) INFO: '
readonly LOG_PREF_ERR='---(X) ERR: '

readonly PIPENV_HOME=pipenv
readonly PIPENV_MD5=.pipenv.md5

function install_pipenv_dependencies {
    export WORKON_HOME="${PIPENV_HOME}"
	curr_md5="$(md5sum < ./Pipfile)"

    # Dependencies were never installed (or deleted manually)
    if ! test -d "${PIPENV_HOME}"; then
        echo "${LOG_PREF_INFO}Installing application dependencies"
        pipenv install --dev

    # Changes detected in application dependencies
    elif ! test "${curr_md5}" == "$(cat "${PIPENV_MD5}" 2> /dev/null)"; then
        echo "${LOG_PREF_INFO}Updating application dependencies"

        pipenv update --dev
        echo "${curr_md5}" > "${PIPENV_MD5}"

    # All good and no updates necessary
    else
        echo "${LOG_PREF_INFO}Application dependencies are up to date"
    fi
}

function set_shell_vi_mode {
    echo -e 'set -o vi\nbind -m vi-insert "\C-l":clear-screen' >> ~/.bashrc
}

function main {
    if test "$#" -lt 1; then
        echo "${LOG_PREF_ERR}No command to execute specified"
        exit 1
    fi

    # Drop directly into shell for tooling debugging
    if test "$1" = '--shell'; then
        exec '/bin/sh'
        exit "$?"
    fi

    install_pipenv_dependencies
    set_shell_vi_mode

    echo "${LOG_PREF_INFO}Executing a target command"
    exec "$@"
}

main "$@"
