# Resumen de la Lectura15
La infraestructura engloba todo lo necesario para ejecutar un app<br>
```bash
            almacenamiento
                    ↓
      computo  → INFRAESTRUCTURA ← red
                    ↑
            seguridad(politicas IAM)
```
Antes se configuraba todo esto desde CLI
## ¿Qué es IaC?
Infraestructura como codigo (infraestructura en archivos) , en este archivo declaramos la infraestructura que queremos<br>
```bash
    pasos ad-hoc            | definicion en archivos
    ssh server                  HCL o JSON(terraform),YAML (ansible)
    yum install nginx           qué recursos queremos
    ...
    crea la red                 "quiero una maquina con ngnix en la 
    luego la maquina                red X "
    despues instala nginx
```
```bash
recurso "aws_instance" "web"   {
    ami = "123"
    instance_type = "t2.micro"
} 
quiero(que debe existir) una instancia EC2 con estas caracteristicas
```

## ¿Qué no es IaC?
Ejecutar *configuracion.sh* sin los principios de IaC
 
## Principios de IaC 
```bash
        Reproducibilidad        Composibilidad
        (entornos identicos)     (no cambio innecesario de estado )
        Idempotencia            Envolvibilidad
```
Mientras Reproducibilidad e Idempotencias nos nos de alguna manera ya conocidas; veamos las dos propiedades nuevas<br>
Para ello revisemos la sintaxis de HCL(Hashicorp..) que es precisamente el lenguaje declarativo de configuracion que usaremos<br>
```bash
tipo_de_bloque "id1" "id2" {
    atributo = valor
    sub_bloques....
}
esto varia un poco dependiendo de que tipo de bloque es especifico se trate
resource tipo_definido_por_un_proveedor nombre_local {
    clave = valor
}
variable nombre_escogido {
    clave = valor  
}
recurso "aws_instance" "web"   {
    ami = "ami-0abcd1234"
    instance_type = "t2.micro"
} 
y module llama a las anteriores como lo haria una funcion
```
Okay, tenemos la sintaxis ,ahora veamos como referenciar los bloques entre si.
![interaccion entre bloques](imagenes/lectura15_sintaxis_2.png)<br>
como se observa ,la variable server_name el disparador para crear un nuevo recurso , si este cambia se rehace el recurso ejecutando el provisionador , quien ejecuta un comando de interés.<br>

## Composibilidad
Se tiene la sintaxis de los bloques y como las variables llamadas en dentro del ambito de los resource, veamos como se pasan los valores ingresados en main.tf hacia los modulos network y compute, lo cual nos muestra la propiedad de  composabilidad 
Ahora bien la COMPOSABILIDAD  se veria del siguiente modo 
![composabilidad](imagenes/lectura15_composabilidad.png)
## Evolvibilidad

En cuanto a la EVOLVIBILIDAD ,se diria que es similar a export una variable en bash para que los procesos hijos lo usen , o parecido a la iyeccion de dependencias .
Entonces esto facilita la extension y adaptacion de la configuracion 
![evolvibilidad](imagenes/lectura15_evolvibilidad.png)

### versionado de cambios
- Separacion de responsabilidades:<br>
    *Variables (network.tf.json)*<br>
    cómputo (main.tf.json)<br> 
    lógica de generación (main.py)
- Parametrizacion : <br>
    *hello_server_local(name="app1", network="net1")*<br>
    hello_server_local(name="app2", network="net2")
- Portabilidad con Docker:<br>
    *docker-compose up --build*

## Por qué usar IaC
Porque da control, velocidad ,  colaboracion y seguridad
- Gestion de cambios
- Retorno de inversion
- Compartir conocimiento 
- Seguridad 

## Herramientas
- Aprovisionamiento
- Gestion de configuracion 
- Construccion de imagenes
### como encajan estas capas en un pipeline 
- Desarrollo  y pruebas locales
- Control de calidad
- Despliegue
- Monitoreo y feedback 

## Escribiendo IaC 
### Expresando cambios en infraestructura
- Edicion declarativa de archivos
- Flujo clasico  init → plan → apply
- Plan como contrato 
### Comprendiendo la inmutabilidad
- Nunca parchear en caliente evitar ssh 
- Construccion de imagenes como paso previo
- Despliegue de blue /green o rolling 
- Remeditacion de drifts
- Migracion desde entornos legados
### Escribiendo codigo limpio de IaC
- Control de versiones como fuente de verdad
- Linting y formateo automatico
- Convenciones de nombrados
- Variables bien estructurados
- Parametrizar dependencias con codigo 
- Manejo seguro de secretos
## Anexos
A. Consistencia entre modulos 
```bash
# modules/network/variables.tf
variable "network_name" {
  description = "Nombre de la red principal"
  type        = string
}

# modules/network/main.tf
# ... recursos de red ...

# modules/network/outputs.tf
output "network_name" {
  description = "Nombre de la red creada o referenciada"
  value       = var.network_name
}
```
B. Variables con HCL y terraform.tfvars 
```bash
# variables.tf
variable "project_id" {
  type        = string
  description = "ID del proyecto"
}

variable "region" {
  type        = string
  description = "Región por defecto"
  default     = "us-central1"
}
....
# terraform.tfvars (ejemplo dev)
project_id  = "demo-devsecops"
region      = "us-central1"
tags        = ["owner:devsecops", "env:dev"]
db_password = "cámbiame"
```
C. Backend remoto y bloqueo de estado<br>
Usar backend remoto y locking <br>
S3 y DynamoDB
```bash
terraform {
  backend "s3" {
    bucket         = "tfstate-demo-devsecops"
    key            = "infra/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "tfstate-locks"
    encrypt        = true
  }
}
```
D. Usar Makefile ,estandariza flujo y facilita CI
```bash
SHELL := /usr/bin/env bash

TF ?= terraform
TF_DIR ?= ./

.PHONY: tools fmt lint init plan apply destroy clean

tools:
	command -v terraform >/dev/null || { echo "Instala Terraform"; exit 1; }
	command -v tflint >/dev/null || { echo "Instala tflint"; exit 1; }
	command -v checkov >/dev/null || { echo "Instala checkov"; exit 1; }

fmt:
	$(TF) -chdir=$(TF_DIR) fmt -recursive

lint: fmt
	tflint --recursive
	checkov -d $(TF_DIR)
...
```
E. Hook pre-commit (formato , lint y seguridad)
```bash
#!/usr/bin/env bash
set -euo pipefail
terraform fmt -recursive
tflint --recursive
checkov -d .
```