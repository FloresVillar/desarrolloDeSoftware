from app.adapters import SecureRequestClient
from app.services import MovieServices





from app.adapters import FakeHttpClient
from app.servcies import MovieServices

fixtures = {"https://api.ejemplo.com/status" : { "ok" : True}}
htpp = FakeHttpClient(fixtures= fixtures) # FakeHttpClient .get_json(url) lookup→fixture[url]  lookup es busqueda por clave en una estrucctura tipo diccionario, tomamos url como clave y recuperar un valor asociado en el dicc fixtures
svc = MovieServices(http=http) 
assert svc.status() == {"ok" : True}
