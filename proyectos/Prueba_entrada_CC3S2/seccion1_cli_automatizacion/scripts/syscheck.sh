#!/usr/bin/env bash
set -euo pipefail
trap 'echo "[ERROR] Falló en línea $LINENO" >&2' ERR

mkdir -p reports

# TODO: HTTP-guarda headers y explica código en 2-3 líneas al final del archivo
{
  echo "curl -I example.com"
  curl -Is https://example.com | sed '/^\r$/d'
  echo
  echo "Explicación (editar): el cliente curl hace una peticion para obtener las cabeceras al dominio en cuestion 
  el resultado de esa consulta (GET) se pasa al comando que edita streams , este borra las lineas vacias
  /PATRON DE BUSQUEDA/ ^ inicio   \r retorno de carro   $ final  luego lo borra"
} > reports/http.txt
# ![sed](https://www.hostinger.com/es/tutoriales/comando-sed-linux)

# TODO: DNS — muestra A/AAAA/MX y comenta TTL
{
  echo "A";    dig A example.com +noall +answer
  echo "AAAA"; dig AAAA example.com +noall +answer
  echo "MX";   dig MX example.com +noall +answer
  echo
  echo "Nota (editar): TTL alto vs bajo impacta en el timepo de vida que ese dominio estara el cache,
  con TTL alto  se hara menos consultas al servidor autoritativo, caso contrario mas consultas."
} > reports/dns.txt

# TODO: TLS - registra versión TLS
{
  echo "TLS via curl -Iv"
  curl -Iv https://example.com 2>&1 | sed -n '1,20p'
} > reports/tls.txt

# TODO: Puertos locales - lista y comenta riesgos
{
  echo "ss -tuln"
  ss -tuln || true
  echo
  echo "Riesgos (editar): Puertos abiertos innecesarios pueden exponer varias puertas de entrada a 
 ataques como inyeccion SQL o csrf"
} > reports/sockets.txt

echo "Reportes generados en ./reports"
