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
    def mostrar_all(self,)  # o mostrar_todos()
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

```
