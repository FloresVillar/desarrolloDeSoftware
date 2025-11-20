## Resumen (a lo sumo) de la lectura 16
En IaC organizar los componentes en achivos HCL , JSON o clases generadoras python => escalabilidad, mantenibilidad y coherencia.

Para recursos "null_resources" <= patrones de diseño clásicos del desarrollo de software .
El proyecto crece → muchas configuraciones → desorden , entonces se precisan metodologias de diseño.

En el caso particular del labo 6:
- Terraform json como proveedor null, se simula aprovisionamiento mediante "local-exec"
- Clases python que generan los bloques JSON de recursos, fabricas,prototipos  y builders.
- Orquestador (main.py) ensambla todos los modulos en un "main.tf.json".

De modo que se verá que cada patron de diseño facilita tareas concretas
Evitar duplicados (Singleton), Representar jerarquías(Composite) , Desacoplar la logica de creacion (Factory) , Reutilizar configuraciones(Prototype) , construir objetos complejos(Builder)

### Patrón Singleton: intancia única garantizada

Lo que se precisa es una unica instancia de clase durante el ciclo de vida de nuestra app, asi como un unico punto de acceso , esto podria usarse en el caso de : 
- Un bucket centralizado de logs
- Una VPC compartida entre varios entornos
- Politicas de seguridad globales

Entonces seria como un atributo de clase(la misma para todas las instancias de una clase) pero aplicado a la instancia de esa clase.
```bash
a = Singleton()
b = Singleton()
c = Singleton()
a is b is c   # es True
#son el mismo objeto en memoria
```
Lo anterior es el fin buscado , pero antes es preciso señalar la sintaxis y convenciones involucradas, para  un ejemplo simplificado todo cuanto se pudo
```bash
class 
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return _intance
```
Entonces en este ejemplo se define un atributo de clase (que será la instancia de clase , la unica) , y se usa un metodo magico que python ejecutara por si mismmo , a saber , __new__, puesto que comienza y termina con __. 

Tiene un parámetro **cls** que sera un argumento, al ser invocado, este no es una palabra reservada pero es una convencion usada , representa a la clase en si misma.

Como python pasa automáticamente la instancia como el primer argumento de los metodos normales **metodo(self)** y pasa la clase **__new__(cls)** como primer argumento de los metodos magicos. Se concluye que **cls** representa la clase.

Entonces **__new__** recibe cls y determina si el atributo de clase no existe, en caso de ser asi la creamos llamando a al metodo __new__ de la clase padre via super(), pues super() devuelve el siguiente objeto del MRO.

Una vez creada devolvemos el atributo (instancia) esto cada vez que se pretenda crear una instancia de la clase en cuestión.

### Patrón Composite: Jerarquías recursivas 
La idea simple es que si varias clases comparten un metodo comun entonces sera otra clase quien agrege objetos de las clases anteriores a una lista , de modo que se recorra la lista ejecutando dicho metodo.
Y esta tercera clase seria el composite
```bash
class File:
    def __init__(self):
    
    def mostrar(self):

class Folder:
    def __init__(self):
    
    def add(self,obj):

    def mostrar(self):

#  y creando los objetos
f1 = File ()
f2 = File()
f3 = Folder()
f3.add(f2)

contenidos = [f1, f3]
# para usar mostrar()
for e in contenidos:
    if e is File
        e.mostrar()
    if e is  Folder
        e.mostrar()
# se tiene que determinar si es File o Folder

```
Entonces usamos composite para lograr lo que se describe al inicio .
```bash
class Composite:   # las clases anteiores podrian heredar de Component, en este caso es mas directo 
    def __init__(self):
        self.lista
    def add(self,obj):
        self.lista.add(obj)
    def mostrar_all(self,)  # o construir_todos()
        conjunto  = {}
        for e in self.lista
            r = e.mostrar()
            conjunto.update(r)
        return conjunto 
```

### Patrón Factory : Delegar Creación 
La esencia es similar al patron anterior en el sentido de que se usara un metodo para construir dentro de clases delegadas. De modo que separamos la logica de la creacion a clases especializadas 


```bash
class Base:
    def construir():
        raise NotImplementedError()
class DataFactory:
    def __init__(self,nombre):
        self.nombre = nombre
    def contruir(self):
        #logica de interes
class RedFactory:
    def __init__(self,cidr):
        self.cidr = cidr
    def construir(self):
        #logica de interes
class ServerFactory:
    def __init__(self,host):
        self.host = host
    def construir(self):
        #logica de interes
```
Y como en el ejemplo de la lectura, el orquestador itera sobre una coleccion de fabricas(las clases delegadas) 
```bash
fabricas = []
for f in fabricas : 
    recurso = f.construir()
    print(recurso)
```

### Patrón Prototype : Clonación de plantillas
El patron permite la clonacion de objetos modificando solo las partes necesarias. Util por ejemplo cuando queremos generar subredes con algunos atributos modificados

```bash
import copy
class Prototype:
    def __init__(self,valor,etiqueta):
        self.valor = valor 
        self.etiqueta = etiqueta
    def clonar(self, **cambios):
        nuevo = copy.deepcopy(self)
        for  clave, valor in changes.items:
            setattr(nuevo,clave,valor)
        return nuevo

proto = Prototype(valor = 100, etiqueta ="BASE")
prot1 = proto.clone(etiqueta = "A")
prot2 = proto.clone(etiqueta = "B",valor = 200)

```
Un poco de la sintaxis **cambios, python convierte a dict los argumentos pasados; mientras que con setttr() se realiza la modificaicon del atributo del nuevo objeto creado.

CABE MENCIONAR QUE ESTOS SON EJEMPLOS DE LOS PATRONES QUE SE ESTAN ESTUDIANDO, EN UN CAMPO DE PROGRAMACION GENERAL, SIN AUN VINCULAR INFRAESTRUCTURA.

### Patron Builder : Construcción paso a paso
Se crea un objeto mediante pasos encadenados
```bash
class ServerBuilder:
    def __init__(self):
        self.config = {}
    def nombre(self,nombre):
        self.config["nombre"] = nombre
    ......
    def construir(self):
        nombre = self.config.get("nombre","servidor")
        print(f"{nombre}...")
        return self.config
```
### Criterios para seleccionar el patron
1. Grado de reutilizacion: 
    - declarar un unico recurso global <= singleton  
    - clonar multiples configuraciones <= prototype
2. Complejidad de configuracion
    - pocas propiedades construccion directa <= factory
    - muchas opciones <= Builder
3. Estructura jerarquicas
    - Varias capas de dependencias (VPC->subredes->intancias) <= Composite
4. Escalamiento y mantenibilidad
    - proyectos pequeños <= Factory y prototype
    - Sistemas empresariales <=Factory y Prototype
5. Pruebas y validacion
    - facilitar test unitarios evitando singleton ocultos <= Builder y Factory
6. Evolucion de proyectos
    - proyecto grande <=Composite + Builder
    - scripts rapidos <= Factory y prototype

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