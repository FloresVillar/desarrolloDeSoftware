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

Entonces **__new__** recibe cls y determina si el atributo de clase no existe, en caso de ser asi la creamos llamando a al metodo __new__ de la clase padre via super(), super() devuelve el siguiente objeto del MRO.

Una vez creada devolvemos el atributo (instancia) esto cada vez que se pretenda crear una instancia de la clase en cuestión.