import random
from faker import Faker 
import pytest

@pytest.fixture(autouse = True)
def _semillas_estables():
    random.seed(123)
    try:
        Faker().seed_instance(123)
    except Exception:
        pass

