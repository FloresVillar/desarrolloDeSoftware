SHELL :=bash
.SHELLFLAGS  := -eu -o pipefail -c
MAKEFLAGS += --warn-undefined-variables --no-builtin-rules
OUT_DIR :=out
SCR_DIR :=src
PYTHON ?=python3

SHELLCHECK := shellcheck

.DELETE_ON_ERROR:

.DEFAULT_GOAL: help


#todos los targets
.PHONY: all build tools lint build test package clean lint benchmark check format help


all: tools lint build test package ## ejecuta todas las tareas 
build: $(OUT_DIR)/hello.txt ## genera el archivo hello.txt 

$(OUT_DIR)/hello.txt:$(SCR_DIR)/saludo.py
	@echo "." $@
	@mkdir -p $(@D)
	$(PYTHON) $< > $@

clean: ## limpia los archivos generados
	@rm -rf $(OUT_DIR)		

help:  ## descripcion de los 1targets
	@grep -E '^[a-zA-Z0-9_-]+:.*##' $(MAKEFILE_LIST) | awk -F ':|##' '{printf "%-12s %s\n",$$1,$$3}'
#↑ aqui va bash -eu -o pipefail -c grep -E '^[a-zA-Z0-9_-]+:.*##' $(MAKEFILE_LIST) | awk -F ':|##' '{printf "%-12s %s\n",$$1,$$3}'
 