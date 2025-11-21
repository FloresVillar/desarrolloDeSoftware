"""Patrón Singleton

Asegura que una clase tenga una única instancia global, compartida en todo el sistema.
Esta implementación es segura para entornos con múltiples hilos (thread-safe).
"""

import threading
from typing import Any, Dict
from datetime import datetime, timezone

class SingletonMeta(type): 
    _instances: Dict[type, "ConfigSingleton"] = {}
    _lock: threading.Lock = threading.Lock()  # Controla el acceso concurrente

    def __call__(cls, *args, **kwargs): 
        with cls._lock:
            if cls not in cls._instances:
                cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class ConfigSingleton(metaclass=SingletonMeta): 
    def __init__(self, env_name: str = "default") -> None: 
        self.env_name = env_name
        self.created_at = str(datetime.utcnow()) # Fecha de creación
        self.settings = {}  # Diccionario para guardar claves y valores
    def set(self, key: str, value: Any) -> None: 
        self.settings[key] = value
    def get(self, key: str, default: Any = None) -> Any: 
        return self.settings.get(key, default)
    def reset(self): 
        self.settings.clear()
