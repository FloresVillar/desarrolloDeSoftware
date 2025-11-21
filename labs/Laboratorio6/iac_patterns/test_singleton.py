import pytest
from .singleton import ConfigSingleton
def test_():
    c1 = ConfigSingleton("dev")
    creado = c1.created_at
    c1.settings["x"] = 1
    c1.reset()
    assert c1.settings == {}
    assert c1.created_at == creado