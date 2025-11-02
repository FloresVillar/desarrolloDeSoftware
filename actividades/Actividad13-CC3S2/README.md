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
```bash
name = "hello-world"
network = "local-network"
ó
name = "staging-server"
network = "staging-network"
y 
terraform apply -var-file=staging.tfvars
```
### versionado de cambios
### Aplicacion de los principios

- Separacion de responsabilidades:<br>
    *Variables (network.tf.json)*<br>
    cómputo (main.tf.json)<br> 
    lógica de generación (main.py)
- Parametrizacion : <br>
    ```bash 
      hello_server_local(name="app1", network="net1")
      hello_server_local(name="app2", network="net2")
    ```
- Portabilidad con Docker: el Dockerfile y docker-compose.yml, garantiza que cualquieer maquina reproduzca e el flujo<br>
    *docker-compose up --build*

## Por qué usar IaC
Porque da control, velocidad ,  colaboracion y seguridad
- ### Gestion de cambios <br>
 **Rastro de auditoria**
 si se cambia el instance_type 
```bash
  t2.micro  a  t3.small en main.tf.json 
```
git diff  <commit1> <commit2>
```bash
diff --git a/app.py b/app.py
index 83db48d..7c5a7b3 100644
--- a/app.py
+++ b/app.py
@@ -10,7 +10,7 @@ def main():
     print("Hello world!")
-    print("Version 1")
+    print("Version 2")
     return True
```
**Revision por pares**
En el pr se incluye un terraform plan
```bash
terraform init    #inicializa el entorno
terraform plan    #genera un plan de ejecucion
Plan: 1 to add, 0 to change, 0 to destroy.
se aprueba (en main)
terraform apply -var-file=staging.tfvars -auto-approve

```
**Rollback instantaneo**
Si un despliegue automatico introduce un error , basta con revertir el commit 
```bash
git revert <SHA del commit> 
terraform vuelve a la version anterior y esto toma algunos minutos en comparacion con horas de reconstruccion manual
```
- ### Retorno de inversion (ROI)
**Despliegue expres** un entorno completo , una red local simulada con null_resource , servidor de prueba se crea en segundos
```bash
terraform apply -auto-approve
``` 
hacerlo manualmente implicaria decenas de clicks en consolas web ssh y validaciones de estado
**Pipelines automatizados**
Integrar Iac en GitHub Actions , GitLab CI o Jenkins  permite que , al hacer merge a main se ejecute automaticamente 

terraform fmt && tflint 
terraform plan 
terraform apply -auto-approve

Con esto se dedica menos tiempo en tareas repetitivas

**escalado horizontal**
si se necesita 5 instancias nuevas para un pico de trafico solo modificamos count=5 y reaplicamos. Terraform crea exactamente las instancias adicionales
sin intervencion manual

- ### Compartir conocimiento
**documentacion viva**
 las variables con nombre claros var.network_name , var.server_name, comentarios en modulos y ejemplos en README.md actuan como guias para miembros nuevos

 **onboarding acelerado** al clonar y ejecutar docker-compose up --build un desarrollador novato levanta un entorno de pruebas indentico al de produccion local 

 **Bibliotecas de modulos reutilizables** almacenados en modulos genericos ej security_group el equipo crea catalogo interno de bloques IaC , fomentando la consistencia entre proyectos
- ### Seguridad
**gestion centralizada de secretos** nunca harcodeamos credenciales, en cambio se integra Vault , AWS SSM o Azure Key Vault, ej el pipeline podria inyectar un token con :
```bash
- name: Login to Vault
  run: vault login -method=github token=${{ secrets.VAULT_TOKEN }}
```
**Revision de politicas** Al difinir roles y permisos de IAM como codigo ,se puede usar herramientas como terraform terraform-compliance para escanear malas configuraciones ej 0.0.0.0/0 no deberia estar en reglas de ssh

**Principio de menor privilegio** al versionar los aws_iam_policy o sus equivalentes, se documenta que permisos necesita cada componente, si una funcion lambda reclama permisos excesivos, el diff muestra que se añadio, evitando por ejemplo que un servicio tenga mas privilegios de los necesarios
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