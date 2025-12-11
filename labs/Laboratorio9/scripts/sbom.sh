#!/usr/bin/env bash
set -euo pipefail
SYFT_BIN="./bin/syft"
IMG="${1:?imagen requerida}"
OUT="${2:?ruta de salida requerida}"

mkdir -p "$(dirname "$OUT")"

echo "[SBOM] Generando SBOM para $IMG en $OUT"
# Ejemplo real:
"$SYFT_BIN" "$IMG" -o spdx-json > "$OUT"

echo "{ \"sbom_for\": \"$IMG\", \"status\": \"PLACEHOLDER\" }" > "$OUT"
