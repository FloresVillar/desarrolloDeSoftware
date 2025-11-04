#retry.py
import random
import time
import requests

def get_with_retry(http, url, attempts=3, base_ms=100, max_ms=1000):
    for i in range(attempts):
        try:
            r = http.get(url, timeout=2.0)
            r.raise_for_status()
            return r
        except requests.RequestException:
            if i == attempts - 1:
                raise
            # jitter con SystemRandom para satisfacer S311
            sleep_ms = min(max_ms, base_ms * (2 ** i)) + random.SystemRandom().randint(0, 50)
            time.sleep(sleep_ms / 1000.0)

#get_retry
#estamos trabajando sobre funciones, no sobre cliente
#envolvemos cualquier oepracion idempotende sin conocer operacion
#git reduce costo de cambio
# sin tocar dominio,
# tiene exponencial backup y ....
#badnit 311
#el servicio depende de abstraccion no de detalles(rquest)

#un callable es cualquier objeto que se llama como fncion
#el dominio no crea clientes completos solo lo que necesita