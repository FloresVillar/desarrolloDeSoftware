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
## Indempotencia
Luego del primer apply el estado local (.terraform.tfestate) guarda el estado del recurso, si volvemos a ejecutar terraform apply ,terraform detecta que no hay cambios entre el JSON, luego no se volvera a ejecutar local-exec<br>
Bueno, entonces para esto presentamos a YAML (YAML ain't markup language)<br>
Describe info estructurada(listas , objetos, valores)
```bash
persona:
  nombre: "P1"
  edad: 25
  habilidades: 
    - Terraform
    - Ansible
```
Ahora es ANSIBLE es la herramienta de automatizacion que usará YAML, de modo que se describa que tareas ejecutar en que servidores<br>
![indempotencia](imagenes/indempotencia.png)
Mientras hosts, become, tasks son palabras reservadas de YAML; apt , service, copy.. son modulos de ansible, como se ve cada modulo tiene sus parametros y hace una tarea especifica<br>
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

- **Aprovisionamiento** , nos provisionamos de infraestructura una nube privada virtual, red, balanceador , base de datos.
![aprovisionamiento](imagenes/provisionamiento.png)
luego 
```bash
terraform init
terraform plan
terraform apply
```
Pero nunca esta de mas detallar como funciona cada comando<br>
```bash
terraform init # prepara el proyecto descargando los providers
providers "aws" {
  region = "us-east-1"
}
resource "aws_instance" {
  ami = "ID"
  instance = "t2.micro" # ami
  tags ".." {
    ...
  }
}
.....

terraform plan # antes de crear recursos vemos que va a hacer terraform 
An execution plan has been generated and is shown below.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # aws_instance.mi_ec2 will be created
  + resource "aws_instance" "mi_ec2" {
      + ami                          = "ami-0c55b159cbfafe1f0"
      + instance_type                = "t2.micro"
      + tags                         = {
          + "Name" = "MiInstanciaTerraform"
        }
    }

Plan: 1 to add, 0 to change, 0 to destroy.

y finalmente 
terraform apply  # aplica los cambios descritos en el plan
```
- **Gestion de configuracion** 
Dejarla en el estado deseado: intalar  paquetes, copiar archivos de configuracion , gestionar servicios<br>
Estado deseado : cada playbook decribe el estado final<br>
Agentes vs agentless: Ansible suele funcionar por SSH<br>
Indempotencia: Aplicada en la maquina recien creada como en aquellas recreadas tras un provisionioning<br>
```bash
# playbook.yml
- hosts: all
  become: true
  vars:
    app_user: deploy
  tasks:
    - name: Crear usuario de la aplicación
      user:
        name: "{{ app_user }}"
        shell: /bin/bash

    - name: Instalar dependencias
      apt:
        name:
          - nginx
          - git
        state: present

    - name: Desplegar código
      git:
        repo: "https://github.com/mi-org/mi-app.git"
        dest: "/home/{{ app_user }}/app"
        version: "main"

    - name: Configurar servicio systemd
      template:
        src: service.j2
        dest: /etc/systemd/system/mi-app.service

    - name: Habilitar y arrancar servicio
      systemd:
        name: mi-app
        enabled: yes
        state: started
```
Como se ve tenemos un play que se aplica a todos los hosts **all** , y con become : true ejecutamos como **root** mediante sudo<br>
Mientras que la palabra reservada **vars** define variables locales al play , app_user será accesible desde las tareas <br>
mediante {{ app_user }}, las tareas cumplen codigo como documentacion, asi que son suficientemente explicitas<br>
![configuracion](imagenes/configuracion.png)
Aun asi veamos algunos detalles, la tarea desplegar codigo 
```bash
- name: Desplegar código
  git:
    repo: "https://github.com/mi-org/mi-app.git"
    dest: "/home/{{ app_user }}/app"
    version: "main"

```
el modulo git clona un repo de Git, dest es la carpeta de destino <br>
La tarea template (plantilla de servicio) copia un archivo de plantilla Jinja2 (.j2) al servidor, procesando variables dentro.
```bash
  [Service]
  User={{ app_user }}
  ExecStart=/home/{{ app_user }}/app/start.sh
```
La siguiente tarea es conocida, el modulo systemd gestiona servicios del sistema (start,stop,restart)<br>
```bash
- name: Habilitar y arrancar servicio
  systemd:
    name: mi-app
    enabled: yes
    state: started

```
y todo se ejecutaria con 
```bash
ansible-playbook -i inventory playbook.yml
```
- **Construccion de imagenes**<br>
Se busca crear artefactos inmutables, contenedores Docker o imagenes VM, con todo preinstalado.<br>
De modo que minimizamos pasos en tiempo de arranque y garantizamos entornos identicos<br>
    - Arranque rapido, el contenedor ya incluye dependencias
    - Reproducibilidad, la imagen es un snapshot de su stack
    - Inmutabilidad, si falla un nodo lanzas otra imagen

Okay ahora hablemos de Docker<br>

**Docker** 
Es una plataforma para emmpaquetar aplicaciones y sus dependencias<br>
En tanto que un contenedor es una "pequeña maquina (vm)" aislada que comparte el kernel de sistema operativo del anfitrion, pero tiene sus propios procesos, sistemas de archivos y red 
![docker](imagenes/docker.png)

Por su parte la sintaxis de Dockerfile
![sintaxis](imagenes/sintaxis.png)

Ejemplo
```bash
FROM python:3.10-slim

# 1. Instala dependencias del sistema
RUN apt-get update && apt-get install -y git

# 2. Crea usuario y directorio de trabajo
RUN useradd -ms /bin/bash deploy
WORKDIR /home/deploy

# 3. Copia código y dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# 4. Define comando por defecto
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
```
obtenemos la imagen , iniciamos el contenedor en el sentido de que ejecutamos comandos en tiempo de construccion (una capa por ejecucion), cambiamos al directorio deploy, copiamos requirements a la imagen, y finalmente ejecutamos el comando luego de construido el contenedor
CMD ejecuta el equivalente a
```bash
CMD gunicorn app:app --bind 0.0.0.0:8000
/bin/sh -c "gunicorn app:app --bind 0.0.0.0:8000"

#un ejemplo mas simple

CMD ["python", "app.py"]
python app.py
```
visualmente
```bash
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8000"]
│      │             │           └── red y puerto
│      │             └── App (módulo:objeto)
│      └── Ejecutable principal (servidor WSGI)
└── Instrucción CMD de Docker
#app.py
from flask import Flask
app = Flask(__name__)
@route('/')
def saludo():
  return "saludos!"
```
docker build -t mi-app:latest .<br>
docker run -d -p 8000:8000 mi-app:latest<br>

el CMD ejecuta dentro del contenedor
```bash
guicorn app:app --bind 0.0.0.0/8000
```
levantamos el servior web flask en http://localhost:8000

**Packer**
Construye imagenes de maquinas virtuales completas<br>
   - Amazon AMI (EC2)
una imagene de todo el sistema operativo(Ubuntu)
```bash
{
  "builders": [
    {
      "type": "amazon-ebs",
      "region": "us-east-1",
      "source_ami": "ami-0abcdef1234567890",
      "instance_type": "t3.micro",
      "ssh_username": "ubuntu",
      "ami_name": "app-{{timestamp}}"
    }
  ],
  "provisioners": [
    {
      "type": "shell",
      "inline": [
        "sudo apt-get update",
        "sudo apt-get install -y nginx git python3-pip",
        "git clone https://github.com/mi-org/mi-app.git /opt/mi-app",
        "pip3 install -r /opt/mi-app/requirements.txt"
      ]
    }
  ]
}
```
packer build packer.json<br>
Arranca una instancia temporal de EC2,ejecuta los comandos de instacion (apt-get, git, pip3..) , se crea una AMI ya configurada y luego terraform puede instanciar la imagen
```bash
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "web" {
  ami           = "ami-0a1b2c3d4e5f6g7h8"  # ←← la AMI creada por Packer
  instance_type = "t3.micro"

  tags = {
    Name = "ServidorConPacker"
  }
}

```
### como encajan estas capas en un pipeline 
- Desarrollo  y pruebas locales: Construyes el contenedor Docker o Packer , ejecutamos el playbook de ansible  sobre el nuestro entorno local(Docker compose)

- Control de calidad , en CI  cada pull request dispara : <br>
      - Linting / formato terraform (terraform fmt)<br>
      - Validacion de playbook Ansible (Ansible-lint)<br>
      - Build de imagenes Docker (docker build --no-cache)<br>
      - Pruebas de integracion "entorno Staging" provisionado con terraform local (null_resource)<br>

- Despliegue : Terraform crea y redimensiona infraestructura en la nube , ansible aplica configuraciones de ultimo milla , el orquestador (kubernetes) arranca contenedores basados en la imagen 
- Monitoreo y feedback : Herramientas de observabilidad(Grafana) validan que todo este en verde, cualquier cambio manual dispara drift , detecatado por terraform plan o inventarios ansible <br>
## Escribiendo la IaC
En Iac plasmamos nuestra insfraestructura en un archivo , de modo que se pueda rastrear su ciclo de vida<br>
Las siguiente pautas permiten trabajar en entornos inmutables y mantener el codigo limpio y sostenible<br>

### Expresando cambios
1. Edicion declarativa cada vez que queremos cambiar algo , por ejemplo el tipo de instancia o el numero de servidores, modificaremos **.tf** o **.tf.json** , no se ejecuta comandos imperativos sino que se declara lo que se quiere
```bash
#si se tenía
resource "tipo" "name_local"{
  tiggeres  ={
      count = "1"  
  }
}
#luego
resource "tipo" "name_local"{
  tiggeres = {
    count = "3"
  }
}

```
2. Flujo clasico : init, plan , apply <br>
    - terraform init , decarga proveedores , inicializa el modulo local y prepara el estado 
    - terraform plan , muestra el reporte linea a linea de lo que se va a crear, modificar o destruir 
    - terraform apply ejecuta esos cambios solos si has validado el plan 

3. Plan como contrato, piensa en terraform plan como un contrato entre tu equipo y la infraestructura , una vez aceptado apply cumple lo pactado , si alguien cambia manualmente  un recurso por fuera (un drift ) el siguiente plan lo detectara 
```bash
# terraform detecta un cambio "out-of-band"
~ null_resource.app
  triggers.count "3" => "1"
```

### Comprendiendo la inmutabilidad
La inmutabilidad es un paradigma clave para entornos de produccion robusto 

1. Nunca parchear en caliente evitar ssh para instalar parches ,en lugar de eso consolida los cambios en una nueva imagen 

2.  Construccion de imagenes como paso previo con Docker o Packer
```bash
FROM ubuntu:20.04 
RUN apt-get update && apt-get install -y nginx=1.18.*
COPY ./app /srv/app
CMD ["nginx","-g","daemon off;"]
```
Entonces cada vez que cambiemos la version de nginx o la aplicacion ,se produ
ce una nueva etiqueta de imagen , por ejemplo registry/myapp:...

3.  Despliegue de blue /green o rolling
    - BLUE/GREEN : despliega la version nueva (green) pruebas de salud, rediges el trafico , luego se descarta la antigua vesrsion (blue)
    - Rolling  ,reemplaza los nodos uno a uno , manteniendo siempre capacidad de servir
4. Remeditacion de drifts(out-of-band) cualquier cambio manual queda fuera del control de IaC , al detectar drift con terraform plan , se puede :
      - Revertir el cambio manual en consola
      - Actualizar el codifgo para que refleje la nueva configuracion deseada 
5.  Migracion desde entornos legados
    - Importacion , usamos terraform import null_resource.app<id> para traer recursos existentes
    - Definicion , codifica en .tf cada recurso importado , por ejemplo 
    ```bash
    resource "nombre_aws" "local" {
      palabra_reservada_aws = "mi-bucket-aws"
      acl = "private"
    }
    ```
    - Verificacion , terraform plan debe reportar "no changes " cuando ya coincida el estado con el codigo
    
### Escribiendo codigo limpio de IaC
1. **Control de versiones** como fuente de verdad: 
    - Se escribe n README.md que explique el flujo completo (init, plan, apply)<br>
    - Trabajamos con ramas de feature y usamos pull request para revisar los cambios
    - Etiquetas (tags) versiones estables de la infraestructura , por ejemplo v1.0.0
2. **Linting y formateo automatico**:
    - Ejecuta en tu CI y local:
      ```bash
        terraform fmt -recursive
        tflint 
      ```
      - configura un hook de Git (pre-commit) que bloquee commits que no pasen estos chequeos
3. **Convenciones de nombrados**, seguir un patron uniforme que refleje proyecto , entorno y tipo de recurso
```bash
projects-env-type-name 
└─ myapp-prod-sg-web
└─ myapp-dev-mullserver
```
De modo que al listar sabremos a que entorno y componente pertenecen

4. **Variables bien estructurados**
    - variables.network.tf.json para red
    - variables.compute.tf.json  para computo
    - Definir descripciones claras y valores por defecto 
    ```bash
    {
      ""variable" :[
        {
         "name" : [
              {
                "type" : "tipo"
                "default" : "nombre"
                "description" : "descripcion ,nombre del servidor principal "
              }
          ]
         },
         {
            "network " : [
              {
                "type" : "string"
                "default" : "local-network"
                "description" : "identificador de la red local"
              }
            ]
         }
      ]

    }
    ```
5. **Parametrizar dependencias con codigo** , si tenemos un script Python (main.py) o un modulo terraform , hacerlo generico! 
```bash
def hello_server(nombre, red, contador = 1):
  #Generar un bloque json que terraform pueda consumir
```
Al cambiar nombre o red ,no se replica plantillas , solo llamamos a la funcion con distintos argumentos<br>

6. **Manejo seguro de secretos**
    - No codificar credenciales en un texto plano
    - En Docker compose o en el pipeline,monta secretos
    ```bash
    services :
     infra:
      enviroment:
       VAULT_ADDR: https://.....
      secrets:
       - vault_token
    secrets:
     vault_token
      file: ./vault_token.txt
    ```
Aqui precisemos que es docker-compose.yml ,  Dockerfile define una sola imagen, crea una sola imagen ej miapp:latest pero en el sistema se tienen mas servicios (base de datos, proxy ,etc) cada servicio necesita su propia imagen , eso se define en archivos separados no con varios FROM <br>
Entonces es docker-compose.yml levanta multiples contenedores a la vez, cada uno con su propia imagen que puede provenir de un Dockerfile distinto<br>
```bash
version : "3.9"
 services:
  web:
   build: . #el Dockerfile de la app
   ports: 
    - "5000:5000"

  db:
   image: postgres:15
   enviroment:
    POSTGRESS_PASSWORD: example
```
se levantan ambos contenedores con **docker compose up**<br>
En lugar de usar
```bash
docker run -p 5000:5000 miapp
docker run -e POSTGRES_PASSWORD=example postgres:15

```
Ademas esta estructura de proyecto es posible
```bash
.
├── web/
│   ├── app.py
│   └── Dockerfile
├── worker/
│   ├── worker.py
│   └── Dockerfile
└── docker-compose.yml

```
El docker-compose.yml puede usar varios Dockerfile tambien
```bash
version: "3.9"
services:
  web:
    build:
      context: ./web
      dockerfile: Dockerfile.web
    ports:
      - "8000:8000"

  worker:
    build:
      context: ./worker
      dockerfile: Dockerfile.worker
```
## Anexos
Se agregan practicas recomendables y artefactos listos para ser usados<br>

A. Consistencia entre modulos , si nuestro modulo network define var.network_name , se exponen con output para que otros modulos los consuman con coherencia<br>

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
OKAY tenemos claro la sintaxis de terraform, algunas de sus palabras reservadas como variable resource cuyos nombres son definidos por el proveedor(ej aws) y tambien tienen un nombre local, ademas sus propiedades como composabilidad . Ademas algunas herramientas y su uso en Devops, ademas docker sus palabras reservadas como FROM RUN CMD, al igual que ansible que usa yml para automatizar la creacion de insfraestructura<br>

Ahora estamos capacitados para resolver la actividad 13<br>
## Fase 0 : Preparacion
1. revisando main.tf.json <br>
```bash
{
  "resource": [
    {
      "null_resource": [
        {
          "hello-server": [
            {
              "triggers": {
                "name": "${var.name}",
                "network": "${var.network}"
              },
              "provisioner": [
                {
                  "local-exec": {
                    "command": "echo 'Arrancando servidor ${var.name} en red ${var.network}'"
                  }
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}

```
el script main.tf.json presenta un recurso  tipo null_resource, con un nombre local hello_resource, el cual tiene un desencadenante y un provisionador , este provisionador ejecuta localmente(local-exec) el comando detallado en este caso un echo sencillo.<br>
```bash
{ resource :[ tipo :[{  disparador :[{}], provisionador:[{}]  }]]}
```
Mientras que network.tf.json , declara las variables name y network, cada uno de los cuales tiene tipo , valor por defecto y una descripcion, recordar que estos son palabras reservadas, mas no sus valores, los cuales los asignamos nosostros.<br>
```bash
{
    "variable": [
        {
            "name": [
                {
                    "type": "string",
                    "default": "hello-world",
                    "description": "Nombre del servidor local"
                }
            ]
        },
        {
            "network": [
                {
                    "type": "string",
                    "default": "local-network",
                    "description": "Nombre de la red local"
                }
            ]
        }
    ]
}

```
```bash
{ "variable" :[ { "v1"        }  , { "v2"         }     ]}
{ "variable" :[ { "v1" : [ {}]}  , { "v2": [ {}]  }     ]}
{ "variable" :[ { "v1" : [ { "type":"string"}]}  , { "v2": [ {"type":"string"}]  }     ]}
```
2. verificando que se puede ejecutar 
**python3 generate_envs.py** <br>
Pero veamos antes algunos detalles del codigo , aunque brevemente<br>
Se crea una lista ENVS con diccionarios como elementos, 
```bash
ENVS[0]
{'name': 'app1', 'network': 'net1'}
```
Cada uno de estos es pasado como argumento a la funcion **render_and_write**  donde se construye la ruta y se crea la carpeta enviroments/app{i} para cada entorno copiando la plantilla de modules/simulated_app/network.tf.json a enviroments/app{i}/network.tf.json con **copyfile()**<br>

Luego generamos el main.tf.json para cada i-entorno. Seguidamente se une a environments/env[i]/ main.tf.json creando la ruta completa **with open(os.path.jooin(),"w")**, luego copiamos config  a esa ruta (archivo) <br>

Finalmente en main.py iteramos en la lista ENVS llamando a la render_and_write para cada elemento(diccionario con nombre y red)<br>

2. verificando que se ejecuta
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio5$ python3 generate_envs.py
Generados 10 entornos en 'environments/'
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio5$ cd environments/app1

esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio5/environments/app1$ ls
main.tf.json  network.tf.json

esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio5/environments/app1$ terraform init

Initializing the backend...
Initializing provider plugins...
- Finding latest version of hashicorp/null...
- Installing hashicorp/null v3.2.4...
- Installed hashicorp/null v3.2.4 (signed by HashiCorp)
Terraform has created a lock file .terraform.lock.hcl to record the provider
selections it made above. Include this file in your version control repository
so that Terraform can guarantee to make the same selections by default when
you run "terraform init" in the future.

Terraform has been successfully initialized!
```
3. Objetivo: conocer la plantilla base
## Fase 1 : Expresando el cambio de infraestructura
- Cuando cambian variables de configuracion Terraform los mapea  triggers que, a su vez , reconcilia el estado (variables -> triggers -> recurso) 
- Actividad 
  - Modificamos modules/simulated_app/network.tf.json 
  - Regenera enviroments/app1 con python generate_envs.py
  - terraform plan
La fase 1 se intento mediante el flujo indicado, sin embargo los resultados fueron reconstruidos de modo que no hubbieron cambios que apreciar<br>
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/Actividad13-CC3S2$ python3 generat
e_envs.py
Generados 10 entornos en 'environments/'
```
Dentro del entorno app1
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/Actividad13-CC3S2/environments/app1$ terraform init
Initializing the backend...
Initializing provider plugins...
#instalando los provider ....
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/Actividad13-CC3S2/environments/app1$ terraform plan

Terraform used the selected providers to generate the following execution plan. Resource  
actions are indicated with the following symbols:
  + create
#mostrando lo que vamos a crear

esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/Actividad13-CC3S2/environments/app1$ terraform apply

Terraform used the selected providers to generate the following execution plan. Resource  
actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # creando ..
```
De modo que terraform guarda el estado en **terraform.tfstate** , entonces al hacer la modificacion en **network.tf.json** que es solo la plantilla donde se definen las variables name y network, luego generando nuevamente con **generate_envs.py** creamos los 10  entornos ;de modo que terraform.tfstate se rehace,entonces no hay cambio alguno que registrar.<br>

Entonces para conseguir el resultado que la guia facilita, se crean los entornos y una vez en app1 ya con los .tf.json (creados y asignados en el cuerpo de generate_env.py ).Se modifica directamente el valor en "triggers" : { "network" : "net1-1"} , manualmente pues aunque las "variable" 's estan definidas en network.tf.json , estan nunca son referenciadas mediante las expansiones "{var.network}" entonces se modifican(como se menciono) directamente en main.tf.json<br>
Luego se consigue, luego del init previo 
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/actividades/Actividad13-CC3S2/environments/app1$ terraform plan
null_resource.app1: Refreshing state... [id=2819289109106705576]

Terraform used the selected providers to generate the following execution plan. Resource  
actions are indicated with the following symbols:
-/+ destroy and then create replacement

Terraform will perform the following actions:

  # null_resource.app1 must be replaced
-/+ resource "null_resource" "app1" {
      ~ id       = "2819289109106705576" -> (known after apply)
      ~ triggers = { # forces replacement
          ~ "network" = "net1" -> "net1-1"
            # (1 unchanged element hidden)
        }
    }

Plan: 1 to add, 0 to change, 1 to destroy.

```
**Pregunta**
- mediante la inspeccion de terraform.tf.state<br>
- Modificar el Json es tal como indica la accion cambiar el valor de alguna clave, mientras que parchear directamente es modificar el estado sin tocar el json.
- Terraform ve el cambio  lo compara con el etado y solo modifica lo necesario.
- Eso es precisamente lo que se hizo.