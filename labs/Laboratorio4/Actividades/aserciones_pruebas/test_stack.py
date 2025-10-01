from unittest import TestCase

from stack import Stack

class TestStack(TestCase):
    """Casos de prueba para la Pila"""

    def setUp(self) -> None:
        """Configuración antes de cada prueba."""
        self.stack = Stack()

    def tearDown(self) -> None:
        """Limpieza después de cada prueba."""
        self.stack = None

def test_push():
    """Prueba de insertar un elemento en la pila."""
    stack = Stack()
    stack.push(1)
    assert stack.peek() == 1 # "El valor recién agregado debe estar en la parte superior"
    stack.push(2)
    assert stack.peek() == 2 #"Después de otro push, el valor superior debe ser el último agregado",

def test_pop(): 
    """Prueba de eliminar un elemento de la pila."""
    stack = Stack()
    stack.push(3)
    stack.push(5)
    assert stack.pop() == 5
    assert stack.peek() == 3  

def test_peek():
    """Prueba de observar el elemento superior de la pila."""
    stack = Stack()
    stack.push(1)
    stack.push(2)
    assert stack.peek() == 2 # "El valor superior debe ser el último agregado (2)"
    assert stack.peek() == 2 # "La pila no debe cambiar después de peek()")

def test_is_empty():
    """Prueba de si la pila está vacía."""
    stack = Stack()
    assert stack.is_empty() == True #self.assertTrue(stack.is_empty(), "La pila recién creada debe estar vacía")
    stack.push(5)
    assert stack.is_empty() == False #self.assertFalse(stack.is_empty(),"Después de agregar un elemento, la pila no debe estar vacía",)
