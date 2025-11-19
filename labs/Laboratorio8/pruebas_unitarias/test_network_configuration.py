#test_network_configuration.py
import json
import pytest
CONFIG_FILE = 'network_config.json' #valida 

@ pytest.fixture(scope="module")
def conf():
    return json.load(open(CONFIG_FILE))

def test_schema_keys(conf):
    assert isinstance(conf, dict)
    assert 'resources' in conf
    for res in conf['resources']:
        assert 'type' in res and 'name' in res #valida type ,name;estatico
#linter → apply