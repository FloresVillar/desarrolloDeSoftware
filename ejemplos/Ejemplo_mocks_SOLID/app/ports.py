#ports.py
from typing import Protocol, Any
#abstraccion es un contrato minimo, si me das algo que cumpla ESTO yo puedo trabajar
class HttpPort(Protocol):
    def get_json(self, url: str) -> Any: ...
