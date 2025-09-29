#!/usr/bin/env bash 
set -o errexit
set -o nounset
set -o pipefail

IFS=$'\n\t'
umask 027 
set -o noclobber #>

PY = "${PYTHON:-python3}"

DIR_SR="src"

tmp="$(mktemp)"

cleanup(){  #limpieza ordenada y rollback
    error="$1"
    rm -rf "$tmp"
    if [ -f "${SRC_DIR}/saludo.py.bak" ];then
        mv -- "${SRC_DIR}/saludo.py.bak" "${SRC_DIR}/saludo.py"
    fi
    exit "$error"
}

trap 'cleanup $?' EXIT INT TERM

check_deps(){
    local -a array_deps=("$PY" grep)
    for dep in "${array_deps[@]}";do
        if ! command -v "$dep" > /dev/null 2>&1;then
            echo "error: $dep no instalado" >&2
            exit 1
        fi
    done
}

run_tests(){
    
}



