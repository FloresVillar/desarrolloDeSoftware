#!/usr/bin/env bash 
set -o errexit
set -o nounset
set -o pipefail

IFS=$'\n\t'
umask 027 
set -o noclobber #>

PY="${PYTHON:-python3}"

SRC_DIR="src"

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

check_deps(){ #checkea dependencias[]
    local -a dependencias=("$PY" grep)
    for dep in "${dependencias[@]}";do
        if ! command -v $dep  >/dev/null   2>&1;then
            echo " $dep no instalado" >&2
            exit 1                                                                                          
        fi
    done
}

run_tests(){
    local archivo="$1"
    local salida=$("$PY" "$archivo")
    if ! echo "$salida" | grep -F -i -q "Saludos,Todos";then 
        echo "Test fallido, salir!" >&2
        mv -- "$archivo" "${archivo}.bak" || true
    exit 2
    fi
    echo "Test pasó: $salida"
}

probando_pipefail(){
    echo "probando pipefail"
    set +o pipefail
    if false | true | false;then
        echo "pipefail sin deteccion de errores en pipeline status(0)"
    fi
    set -o pipefail 
    if false | false | true;then
        echo ".."
    else 
        echo "pipefail con deteccion de errores en pipeline status (1)"
    fi
}   
 probando_noclobber(){
    cat <<'EOF' >|"$tmp"
    linea1 
    linea2
    linea3
    linea4
EOF
}

check_deps
run_tests "${SRC_DIR}/saludo.py"
probando_pipefail
