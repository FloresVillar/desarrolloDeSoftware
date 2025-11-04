#main.py
# se importa adapters
from .adapters import FakeHttpClient
#que hhtp se inyecta
#el framework orquesta el ciclo de vida de dobles IoC
#el endpont decide que implementar?

def main():
    fixtures = {"https://api.ejemplo.com/status": {"ok": True, "service": "up"}}
    http = FakeHttpClient(fixtures)
    from .service import MovieService#ioc un framework llama a tu codigo y solo implemento... dip :pricipio de diseño , di:tecnica par dar dependecias desde afuera ,fabrica,contenedor , es una forma concreta de ioc ,quien crea las dependencias
    svc = MovieService(http)
    print(svc.status())
#
if __name__ == "__main__":
    main()
# from app.adapters import SecureRequestClient
# from app.service import MovieSevices
# se usa httpPort internamente

#http = SecureRequestClient() que implementacion usar par el puerto, se elige el real pero pdria haber sido el fake
#svc = MovieServices(http=http)  el servicio ya puee pedir get_json
#print(svc.status())   

#el composicion make 