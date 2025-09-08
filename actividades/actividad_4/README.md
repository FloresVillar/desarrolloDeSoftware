### Comandos linux para devsecops
situar CLI como herramienta para automatizar tareas:
- marco teorico
- manejo solido de cli
- 

**satanizador?**
1. 
``sed -E \
  -e 's/(password|token|secret)/[REDACTED]/gI' \
  -e 's/\b(pass(word)?|token|secret|api[-_]?key)\b[[:space:]]*[:=][[:space:]]*[^[:space:]]+/\1: [REDACTED]/gI' \
  evidencias/sesion.txt > evidencias/sesion_redactada.txt``
  clave - valor, -E aactiva expesiones regalres, gI aplica a todos las ocurrencias en modo case-inensitive(mayusculas y minuscuclas)
  primera regla:``s/(password|token|secret)/[REDACTED]/gI`` 
  segunda: busca las palabras password tokens :=
  la profundidad del ccodigo fuente va mas alla de escribir un simple script, la parte de configuraciones , contenedores ,se trabajan de esta forma, usamos sed para ocultar datos sensibles
  ectended regular expresion , permite utilizar los ( ) y  |  sin escapes, eje: si ``-e s/../flags``
  esto define una sustitucion
  ``s/REGEX/REEMPLAZO/flags``
  que es lo que se hace en esta linea sed -E
  -e 's/(password|token|secret)/[REDACTED]/gI , primera sustituion
  tengo pass token secret y cual es el reemplazo ,es REDACTED 
  tngo gI g todas las apariciones en linea, I sendible a mayucculas y minsulas, pass ,token y secret pasan  a REDACTED

  la segunda parte 

`` -e 's/\b(pass(word)?|token|secret|api[-_]?ke`y)\b[[:space:]]*[:=][[:space:]]*[^[:space:]]+/\1: [REDACTED]/gI``
  clave= valor clave:valor
que hace ↑ trabajamos con clave valor clave vlaor , hay una letra \b 
cuando trabajms con set   s/../.../ gI esto es una sustitucion de set, ``s/\b(pass(word)?|token|secret|api[-_]?key)\b`` frintera de trabajo alrededor de las claves sendibles, captura api-key o api_key ``api[-_]?key``
``[[:space:]]*[:=][[:space:]]`` espacios opcionales
``[^[:space:]]`` lo mismo 
luego el texto ya tranformado en texto redactado
un sanitizador es un proceso limpia o neutraliza datos peligrosos o senisblees antes de compartirlos o procesaarlos
que hace en el codig fuente. uamos sed y grep acutando como sanitizadores, redactaremos secretos etc
