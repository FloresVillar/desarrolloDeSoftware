APP_NAME ?= miapp2
DOMAIN ?= miapp2.local
PORT ?=8081
VENV :=actividad_2
MESSAGE ?=hoooola
RELEASE ?=v0

VENV_BIN :=$(VENV)/bin
PY :=$(VENV_BIN)/python

##------lanzando la applicacion make run
.PHONY: run
run:
	@echo "iniciando la aplicacion en http://0.0.0.0:$(PORT)"
	@PUERTO=$(PORT) MENSAJE=$(MESSAGE) LANZAMIENTO=$(RELEASE) $(PY) app2.py

##--- activando la configuracion Nginx----
## sudo cp miapp2.conf /etc/nginx/sites-available/	
## ln -s /etc/nginx/sites-available/miapp2.conf /etc/nginx/sites-enabled/
## sudo nginx -t    				sin errores
## sudo systemctl reload  nginx    	recargando

#este target no es un archivo sino una tarea

NGINX_SITIOS_DISPONIBLES :=/etc/nginx/sites-available/$(APP_NAME).conf
NGINX_SITIOS_PERMITIDOS :=/etc/nginx/sites-enabled/$(APP_NAME).conf

OPENSSL :=$(shell command -v openssl 2>/dev/null)
NGINX    := $(shell command -v nginx 2>/dev/null)

CERT_DIR :=certs
CRT_FILE :=$(CERT_DIR)/$(DOMAIN).crt
KEY_FILE :=$(CERT_DIR)/$(DOMAIN).key
NGINX_CERT_DIR := /etc/ssl/miapp2

.PHONY: nginx
nginx:
	@if [ -z "$(NGINX)" ]; then echo "nginx no encontrado (omitiendo)"; exit 1; fi
	@sudo mkdir -p $(NGINX_CERT_DIR)
	@if [ -f "$(CRT_FILE)" ] && [ -f "$(KEY_FILE)" ]; then \
	  sudo cp $(CRT_FILE) $(NGINX_CERT_DIR)/$(DOMAIN).crt; \
	  sudo cp $(KEY_FILE) $(NGINX_CERT_DIR)/$(DOMAIN).key; \
	else echo "Faltan certificados. Ejecuta 'make tls-cert' primero."; exit 1; fi
	@sudo cp nginx/miapp2.conf $(NGINX_SITIOS_DISPONIBLES)
	@sudo ln -sf $(NGINX_SITIOS_DISPONIBLES) $(NGINX_SITIOS_PERMITIDOS)
	@sudo nginx -t
	@sudo systemctl reload nginx 
	@echo " NGINX recargado prueba http://$(DOMAIN)"


.PHONY:	tls-cert 
tls-cert:
	@[ -n "$(OPENSSL)" ] || {echo "openssl no hallado";exit;1}
	@mkdir -p $(CERT_DIR)
	@if [ ! -f "$(KEY_FILE)" ] ; then \
		$(OPENSSL) req -x509 -nodes -newkey rsa:2048 \
			-keyout $(KEY_FILE) -out $(CRT_FILE) -days 365 \
			-subj "/CN=$(DOMAIN)"; \
		echo "certificado creado $(CERT_DIR)/"; \
	else echo "certificado ya existe en $(CERT_DIR)/";fi  

