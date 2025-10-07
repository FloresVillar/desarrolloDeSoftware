#main.py
# se importa adapters
from .adapters import FakeHttpClient

def main():
    fixtures = {"https://api.ejemplo.com/status": {"ok": True, "service": "up"}}
    http = FakeHttpClient(fixtures)
    from .service import MovieService
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