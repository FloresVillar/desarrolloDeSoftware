
## Resumen (a lo sumo) de la lectura 17

### Patrones de dependencia en IaC
Se tiene que definir como fluyen los datos y el orden de creacion,para este fin se recurre a patrones de dependencias que imprimen un orden logico y desacoplo en los modulos IaC
**Relaciones unidireccionales**
```bash 
---------------------                ----------------------
|  modulo RED        | subnet_id     | modulo   COMPUTO   |
|que genera subnet_id|  → → →        |que lanza servidores|
|                    |               |en esta subred      |
---------------------|               ---------------------

module "computo" {
    subnet_id = module.red.subnet_id
}
```
1. Modulo de almacenamiento y politicas:
```bash
resouce "aws_s3_bucket" "servicio_de_almacenamiento" {
    bucket = var.bucket_name # solo expone el nombre
}

output "bucket_arn" {
    value = aws_s3_bucket.data.arn
}

variable "bucket_arn" {
}

resource "aws_aim_policy" {
    policy = jsonencode ({Stament = [{
                            Action = ["s3:GetObject"] 
                            Effect = "Allow" 
                            Resource = ["${var.bucket_arn}"]}]}) # la politica iam recibe este nombre
}
El flujo va del bucket a la politica , nunca al reves
```
2. Colas de mensajes y consumidores
```bash
queue.tf (produce ARN o URL de la cola)→ consumer.tf (consume esa URL) 
def crea_cola():
    return {"queue_url" : ""https://..}}
def crea_connsumidor(queue_url):
    deploy_consumer(service_name="worker",target_queue=queue_url)
    #placeholder, nombre simbolico ,crea funcion Lambda que escucha consumidor
#el flujo unidireccional
info_cola = crear_cola()
crear_consumidor(info_cola["queue_url"])
```

3. Base de datos y capa de aplicacion 
Un modulo de base de datos (db.tf) expone una cadena de conexion → inyectar la cadena en el despliegue de la applicacion (app.tf) . Asi evitamos que la pp intente arrancar sin la base de datos 

4. Testeo Aislado
```bash
terraform apply -var "subnet_id=subnet-....." #asi se prueba solo el modulo computo 
```
Aqui se detalla la sintaxis de **terraform apply -var** 
pasamos el valor de subnet_id desde CLI 
y luego en el modulo computo tendriamos algo asi 
```bash
#en modulos/computo
#var.tf
variable "subnet_id" {

}
#main.tf
resource "aws_instance" "vm" {
.....
    subnet_id = var.subnet_id
}

#luego desde algun local-dev
#terraform apply -var "..."

#var.tf
variable "subnet_id" {}
#main.tf
module "computo" {
    source = "./modules/computo"
    subnet_id = var.subnet_id # pasamos al modulo computo (a su main.tf)
}
```
Entonces con realaciones unidireccionales: Eliminamos ciclos en el grafo de dependencias, facilitamos el calculo automatico de ordenes de provision , mejoramos la mantenibilidad pues cada modulo tiene una interfaz clara  , permite test modulares.

### Inyeccion de dependencias
Se necesita desacoplar, para tal fin se usa DI, IoC, DIP.
Como se vio en el ejemplo anterior , sera un orquestador quien pase los valores de los parametros hacia los modulos.Es el orquestador quien usa el principio IoC y decide el flujo, usando en este contexto DI para pasar parametros a los modulos.
Veamos claramente IoC  y Di 
```bash
IoC == QUIEN MANDA "el modulo no controla el flujo"
#IoC
module "red" {
    source = "./modulos/red"
    cidr_block = var.vpc.cidr  # ← DI
}
```
Pero pareciera que IoC y DI fueran uno mismo, no es asi, veamos los contraejemplos de ello
```bash
### IoC sin DI 
class Servicio:
    def __init__():  
        self.db = Data() # sin DI
    def run():
        db.query()
Class Data:
    def query():

def framework(serv):
    manejador =serv()
    manejador.run()
#en main
framework(Servicio)
### DI sin IoC
class Servicio:
    def __init__(db):
        self.db = db
    def run():
        self.db.query()
#en main
db = Data()
servicio = Servicio(db) # ← DI
servicio.run() # ← controlamos 
### IoC con DI
class Servicio:
    def __init__(db):
        self.db = db
    def run():
        self.db.query()
def framework(serv):
    manejador=serv(Data())
    manejador.run()
#en main
framework(servicio)
```
**Inversion de Dependencias(DIP)**
Se eleva la resiliencia,todo depende de abstracciones, los modulos de alto nivel (orquetador) y los de bajo nivel(modulo de base de datos) no de implementaciones concretas.
Si se migra de la nube a docker, o de S3 a un almacenamiento local , bastará con crear una implementacion de esa abstracción.
Un ejemplo muy minimalista seria
```bash
# DI pero sin DIP
class Servicio:
    sef __init__(db:Data):
        self.db = db
#DI + DIP
class Servicio:
    sef __init__(db:DataInterface):
        self.db = db
```
El ejemplo 
```bash
class RealDatabase:
    def connect(self, url): ...

class MockDatabase:
    def connect(self, url): return InMemoryDB()

def main(db_client):
    conn = db_client.connect(db_client.url)
    # lógica de despliegue…

# En producción
main(RealDatabase(url="postgres://..."))
# En test
main(MockDatabase(url="in-memory"))
```
### Patrones Facade, Adapter y Mediator en IaC
**FACADE** <br>
Facade ofrece una interfaz simple para el usuario. Seria como pasar parametros a funcion y que se construya lo que se quiere en esas funciones.
```bash
module "storage_secure" {
  source           = "./modules/storage-facade"
  name             = "my-data-bucket"
  region           = "us-east-1"
  logs_retention   = 30
}
#es lo que ejecuta el usuario
```
Pero internamento esto es lo que hace
```bash
storage-facade/
├── main.tf
├── variables.tf
└── outputs.tf
#variables
variable "name" {}
variable "region" {}
variable "logs_retention" {
  default = 30
}
#en main.tf internamente crea el bucket y mas bloques
resource "aws_s3_bucket" "this" {
  bucket = var.name
  region = var.region
}
#outputs.tf
output "bucket_arn" {
  value = aws_s3_bucket.this.arn
}

output "bucket_name" {
  value = aws_s3_bucket.this.bucket
}
...
# que luego son referenciados en el module "storage-facade" usando el atributo  source con la ruta del modulo como valor 
```

**ADAPTER**<br>
lo que tenemos (JSON, API) ---adapter---lo que el sistema espera (Terraform , Pulumi)
```bash
#tenemos
{
    "read":["dev"],
    "write":["ops"]
}
#
def adapter(args):
    lista = []
    mapa = {
        "read": ["s3:GetObject"],
        "write": ["s3:PutObject"]
    }
    for a,b in args.items():
        lista.append({
            "actions":mapa.get(a,[]),
            "principals":b
        })
    return {"aws_iam_policy":{"example":{"stament":lista}}}
#en main
argss = {"read":["dev"],"write":["ops"]}
terraform = adapter(argss)
```
Ahora si se cambia a pulummi el return es lo que se modifica
```bash
return PulumiIAMPolicy(
        name="example",
        statements=lista
    )
```
**Mediator**<br>
Mediator centraliza la coordinacion entre varios modulos. Cada modulo no se comunica con los demas, el mediator orquesta el flujo.
```bash
class InfraMediator:
    def deploy_dns(self, record_name):
        lb = self.deploy_load_balancer()
        servers = self.deploy_servers(lb)
        self.configure_firewall(servers)
        self.setup_network()
        return self.create_dns_record(record_name, lb.endpoint)
```
# Laboratorio7-CC3S2

## Fase 1 : Relaciones unidireccionales
1. Inspección
```bash
├── Inversion_control
│   ├── Instrucciones.md
│   ├── main.py
│   ├── main.tf.json
│   ├── Makefile
│   └── network
│       ├── network_outputs.json
│       ├── network.tf.json
│       ├── terraform.tfstate
│       └── terraform.tfstate.backup
```
- Para network.tf.json , se tienen 2 recursos
```bash
.."resource" : {
    "tipo 1": {
        "recurso1" :{}
        }  ,
    "tipo 2": {
        "recurso2" :{}
    }
}
```
En este caso corresponden a "network" tipo "null_resource" y "network_state" tipo "local_file. En cuanto a las dependencias explicitas en el campo "depends_on"
```bash
"depends_on": ["null_resource.network"]  # local_file.network_state depende de null_resource.network
```
- Para main.tf.json
En este caso se tiene un ambito global de recursos (resource block map), donde se declaran los recursos, "null_resource" ,quien genera un nuevo mapa (el resource type map) ,el ambito para este tipo de recurso,las claves declaradas seran recursos de este tipo;lo cual se hace seguidamente declarando la instancia como tal ,a saber "hello_world".
```bash
{
    "resource":{
        "null_resource":{
            "hello_world":{
                #no hay dependencias explicitas
            }
        }
    }
}
```
2. Ejercicio practico
Descargamos los providers:
```bash
"required_providers": {
      "null":  { "source": "hashicorp/null",  "version": "~> 3.2" },
      "local": { "source": "hashicorp/local", "version": "~> 2.5" }
```
Esto se hace via init
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio7/Inversion_control/network$ terraform init
Initializing the backend...
Initializing provider plugins...
- Reusing previous version of hashicorp/null from the dependency lock file
- Reusing previous version of hashicorp/local from the dependency lock file
- Installing hashicorp/null v3.2.4...
- Installed hashicorp/null v3.2.4 (signed by HashiCorp)
- Installing hashicorp/local v2.5.3...
- Installed hashicorp/local v2.5.3 (signed by HashiCorp)

Terraform has been successfully initialized!
```
Luego levantamos la infraestructura con apply sin pedir confirmacion
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio7/Inversion_control/network$ terraform apply -auto-approve
null_resource.network: Refreshing state... [id=6271637016324757625]
local_file.network_state: Refreshing state... [id=d9e6632b7b6fe51a56c55fab21bc32b9df7fc2c0]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the
following symbols:
-/+ destroy and then create replacement

Terraform will perform the following actions:

  # null_resource.network must be replaced
-/+ resource "null_resource" "network" {
      ~ id       = "6271637016324757625" -> (known after apply)
      ~ triggers = { # forces replacement
          ~ "render_time" = "2025-11-03T20:44:13Z" -> (known after apply)
        }
    }

Plan: 1 to add, 0 to change, 1 to destroy.
null_resource.network: Destroying... [id=6271637016324757625]
null_resource.network: Destruction complete after 0s
null_resource.network: Creating...
null_resource.network: Creation complete after 0s [id=8660587588827423380]

Apply complete! Resources: 1 added, 0 changed, 1 destroyed.
```
En este punto surge una duda, init descarga los providers y ese bloque esta declarado dentro de network.tf.json para el ambito de "terraform" y seguidamente el "required_providers" , quien contiene en su ambito las fuentes de los recursos. Pero por qué main.tf.json no declara un bloque "terraform" : { "required_providers"}, no es necesario , terraform buscara en los .tf.json el los providers y solo hace falta declararlos una vez.

Ahora para ejecutar "make all", fue un embrollo, dentro de Inversion_control/network/ se descargan los providers(bootstrap) y levanta la infra de forma manual, luego en Inversion_control/ automatizamos la ejecucion. Pero un detalle importante respecto a "local-exec" :{
    "command" : "echo ...."
}
en bash echo -e "\(\)" es perfectamente valido , entonces usamos ese (?) para escapar de los caracterers especiales, que la shell interpretaria de otra manera, en esta caso los parentesis son subshell(recordar el comando de sustitucion en un .sh).Con este escape terraform  ejecutara local-exec de forma correcta. Finalmente se tendrá **"command": "echo \"Creando servidor hello-world en subred hello-world-subnet (CIDR 10.0.0.0/16, zona local)\""**

Entonces make all ejecuta las recetas 
```bash
    all : prepare network server
    prepare: #crea las carpetas 

    network: # crea subcarpetas 

    server: # init apply
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio7/Inversion_control$ make all
cd network && TF_DATA_DIR=/home/esau/desarrolloDeSoftware/labs/Laboratorio7/Inversion_control/.terraform TF_PLUGIN_CACHE_DIR=/home/esau/desarrolloDeSoftware/labs/Laboratorio7/Inversion_control/.terraform/plugin-cache TMP=/home/esau/desarrolloDeSoftware/labs/Laboratorio7/Inversion_control/.terraform/tmp TEMP=/home/esau/desarrolloDeSoftware/labs/Laboratorio7/Inversion_control/.terraform/tmp terraform init -upgrade -no-color && \
TF_DATA_DIR=/home/esau/desarrolloDeSoftware/labs/Laboratorio7/Inversion_control/.terraform TF_PLUGIN_CACHE_DIR=/home/esau/desarrolloDeSoftware/labs/Laboratorio7/Inversion_control/.terraform/plugin-cache TMP=/home/esau/desarrolloDeSoftware/labs/Laboratorio7/Inversion_control/.terraform/tmp TEMP=/home/esau/desarrolloDeSoftware/labs/Laboratorio7/Inversion_control/.terraform/tmp terraform apply -auto-approve -no-color
# para cada DIR_ACTUAL (CURDIR) se crea .terraform y subcarpetas donde se guarda info del estado (/) , plugins providers (/plugins-cache) y operaciones intermedias (tmp/)
Initializing the backend...
Initializing provider plugins...

...
Finding hashicorp/local versions matching "~> 2.5"...
- Finding hashicorp/null versions matching "~> 3.2"...
- Using previously-installed hashicorp/local v2.6.1
- Using previously-installed hashicorp/null v3.2.4
..
  # null_resource.network must be replaced
-/+ resource "null_resource" "network" {
      ~ id       = "8820400861797525431" -> (known after apply)
      ~ triggers = { # forces replacement
          ~ "render_time" = "2025-11-23T19:40:17Z" -> (known after apply)
        }
    }
    ...
Plan: 1 to add, 0 to change, 1 to destroy.
null_resource.hello-world: Destroying... [id=5457904178799376462]
null_resource.hello-world: Destruction complete after 0s
null_resource.hello-world: Creating...
null_resource.hello-world: Provisioning with 'local-exec'...
null_resource.hello-world (local-exec): Executing: ["/bin/sh" "-c" "echo \"Creando servidor hello-world en subred hello-world-subnet (CIDR 10.0.0.0/16, zona local)\""]
null_resource.hello-world (local-exec): Creando servidor hello-world en subred hello-world-subnet (CIDR 10.0.0.0/16, zona local) 
null_resource.hello-world: Creation complete after 0s [id=5846758902788901647]

Apply complete! Resources: 1 added, 0 changed, 1 destroyed
```
## Fase 2 : Inyeccion de dependencias
1. Inversion de control , inversion de dependencias

Se estudia **main.py** "en caliente",  se tiene una variable global FILE (macro?) que corresponde al .json output para la network. En tanto que clase NMOuput recibe FILE como argumento, se convierte a un path via Path, pues asi se usaran los metodos de un objeto archivo(?), si la ruta no existe se lanza un error. Caso contrario se lee el contenido de esa ruta **data =json.loads(path.read_text())**. En el bloque **try** asigna a las atributos de instancia(objeto?) name y cidr de **data["outputs"]["name"]["value"]  y ["outputs"]["cidr"]["value"]** 

En tanto la clase SFModule , el constructor recibe name zone y el FILE como argumentos y asignamos esos valores a los atributos de instancia; se crea red como una instancia de la clase anterior. Asimismo el atributo recursos llama a su metodo "build()" . Build usa la sintaxis vista, se declara el block map "resource" , el type map "null_resource" , se declara el nombre self._name dentro {} los diparadores y los provisioner. Dentro de provisioner ejecutamos el local-exec : { "command" : ....mostramos info (ejecutar comando si se quiere)}

Okay, desde luego , los terminos tecnicos seran incluidos más adelante.

2. Ejercicio practico

Ahora dentro del type map ,agregamos un nuevo recurso con sus propios  "triggers "y "provisioner" 
```bash
class ServerFactoryModule:
    """Define un null_resource que simula un servidor ligado a la subred."""
    def __init__(self, name_red,name_server, zone="local", outputs_path=OUTPUTS_FILE):
        self._name_red = name_red
        self._name_server =name_server
        self._zone = zone
        self._network = NetworkModuleOutput(outputs_path)
        self.resources = self._build()

    def _build(self):
        return {
            "resource": {
                "null_resource": {
                    self._name_red: {
                        "triggers": {
                            "server_name": self._name_red,
                            "subnet_name": self._network.name,
                            "subnet_cidr": self._network.cidr,
                            "zone": self._zone
                        },
                        "provisioner": [{
                            "local-exec": {
                                "command": 
                                    f'echo "Creando red {self._name_red}, en subred {self._network.name} ,(CIDR {self._network.cidr}, zona {self._zone})"'
                            }
                        }]
                    },
                    self._name_server: {
                        "triggers": {
                            "server_name": self._name_red,
                        },
                        "provisioner": [{
                            "local-exec": {
                                "command": 
                                    f'echo "Creando server {self._name_red}"'
                            }
                        }]
                    }
                }
            }
        }

```
los valores para los campos de los bloques se inyectan como argumentos.
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio7/Inversion_control$ python main.py
main.tf.json generado.
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio7/Inversion_control$ terraform init
Initializing the backend...
Initializing provider plugins...
- Reusing previous version of hashicorp/null from the dependency lock file
- Using previously-installed hashicorp/null v3.2.4

Terraform has been successfully initialized!
..
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio7/Inversion_control$ terraform apply
null_resource.hello-world: Refreshing state... [id=708224974330177754]
null_resource.server: Refreshing state... [id=3061381188353554108]

No changes. Your infrastructure matches the configuration.
```
Nuevamente se ejecuta la receta all prepare , network , server 
```bash
esau@DESKTOP-A3RPEKP:~/desarrolloDeSoftware/labs/Laboratorio7/Inversion_control$ make all
cd network && ...
 Finding hashicorp/null versions matching "~> 3.2"...
- Finding hashicorp/local versions matching "~> 2.5"...
- Using previously-installed hashicorp/null v3.2.4
- Using previously-installed hashicorp/local v2.6.1
...
null_resource.hello-world: Refreshing state... [id=708224974330177754]
null_resource.server: Refreshing state... [id=3061381188353554108]

No changes. Your infrastructure matches the configuration.

Terraform has compared your real infrastructure against your configuration and found no differences, so no changes are needed.

Apply complete! Resources: 0 added, 0 changed, 0 destroyed
```

## Fase 3 : Patrón Facade 
