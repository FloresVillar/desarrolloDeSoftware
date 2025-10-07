#service.py
from .ports import HttpPort

class MovieService: #es la logica de dominio, define QUE HAY QUE HACER , ej traer un status, no como se abre a red
    def __init__(self, http: HttpPort):
        self.http = http
    def status(self):
        return self.http.get_json("https://api.ejemplo.com/status")
#el servicio no sabe si abre a http real, solo conoce el contrato json 
# luego en adapter

#COMPOSICION ROOT punto de arranque real/pruebas
# svc =MovieService(http = SecureRequestClient()) va a prodccion 
# svc  =MovieService(http = FakerHttpClient(fixtures=)) va a prodccion 
#no implementa (recibe) request DI inyeccion DIP depende de abstracciones

# inmutabilidad
# svc = MovieService(http=FakerHttpClient())) 
# svc.http = SecureRequestClient()
# 
#def funcion_status(http:HttpPort,url:str): valido con funciones utilitarias
# peero si queremos fabricar instancias con politicas?

#class httpFactory(Protocol) -> HttpPort: ..
#el servicio depende de una interfaz y no de request directamente
#por ello se puede inyectar