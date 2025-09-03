APP_NAME ?= miapp2
DOMAIN ?= miapp2.local

NGINX_SITIOS_DISPONIBLES :=/etc/nginx/sites-available/$(APP_NAME).conf
NGINX_SITIOS_PERMITIDOS :=/etc/nginx/sites-enabled/$(APP_NAME).conf

##--- activando la configuracion Nginx----
## sudo cp miapp2.conf /etc/nginx/sites-available/	
## ln -s /etc/nginx/sites-available/miapp2.conf /etc/nginx/sites-enabled/
## sudo nginx -t    				sin errores
## sudo systemctl reload  nginx    	recargando

#este target no es un archivo sino una tarea
.PHONY: nginx
nginx:
	@sudo cp nginx/miapp2.conf $(NGINX_SITIOS_DISPONIBLES)
	@sudo ln -sf $(NGINX_SITIOS_DISPONIBLES) $(NGINX_SITIOS_PERMITIDOS)
	@sudo nginx -t
	@sudo systemctl reload nginx 
	@echo " NGINX recargado prueba http://$(DOMAIN)"

##------lanzando la applicacion make run
.PHONY: run
run:
	@echo "RUN"
