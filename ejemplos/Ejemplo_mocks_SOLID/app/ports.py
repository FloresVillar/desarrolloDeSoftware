#ports.py
from typing import Protocol, Any
#abstraccion es un contrato minimo, si me das algo que cumpla ESTO yo puedo trabajar
class HttpPort(Protocol):
    def get_json(self, url: str) -> Any: ...

#sepodria implementar hhtp client
#decorador que envuelve a cliente

#lis coft cuaquier imlmentacion de httpportp puede sustituir a otra sin romoper
#dip el dominio depende de abstaracciones no de detalles
