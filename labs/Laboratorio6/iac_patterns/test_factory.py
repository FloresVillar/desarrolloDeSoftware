import pytest
from .factory import *
formato = '%Y%m%d'
obj = TimeNullResourceFactory()
resultado = obj.crear("fabrica_prueba",formato)
print(resultado)
