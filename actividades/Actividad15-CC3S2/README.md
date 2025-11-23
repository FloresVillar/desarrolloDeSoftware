
## Resumen (a lo sumo) de la lectura 17

### Patrones de dependencia en IaC
Se tiene que definir como fluyen los datos y el orden de creacion,para este fin se recurre a patrones de dependencias que imprimen un orden logica y desacoplo en los modulos IaC
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
#internamente crea el bucket y mas bloques
resource "aws_s3_bucket" "this" {
  bucket = var.name
  region = var.region
}
...
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
