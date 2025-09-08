SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
VENV :=seccion_1
VENV_BIN :=$(VENV)/bin
PY := $(VENV_BIN)/python3
PIP := $(PY) -m pip

#de la experiencia en la actividad_2 cada target envuelve una funcion
#se separa en varios targets, la idea es automatizar la ejecucion de comandos de terminal
#las tareas repetitivas ya no son hechas manualmente  
#se hace el siguiente flujo preparar(librias) → tools(verificar que todo este instalado)→ report (ejecutar los bloques bash que generar los txt con los reportes  )
.PHONY: help tools report all
help: ## Mostrar ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | sed 's/:.*##/: /'

.PHONY: tools
tools: ## Verifica binarios requeridos
	@for b in git bash make python3 pytest curl dig ss jq; do \
	  command -v $$b >/dev/null || { echo "Falta $$b"; exit 1; }; \
	done
	@echo "OK herramientas"

.PHONY: report
report: ## Genera reportes HTTP/DNS/TLS/puertos
	@bash scripts/syscheck.sh

.PHONY: all
all: preparar tools report ## Ejecuta todo

.PHONY: preparar
preparar:
	@echo "instalando pytest"
	@$(PIP) install --upgrade pip
	@$(PIP) install pytest pytest-cov 

#se automatiza la instalacion de pytest , jq si debe ser instalado pues requiere contraseña