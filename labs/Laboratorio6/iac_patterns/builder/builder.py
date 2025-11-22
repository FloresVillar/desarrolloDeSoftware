from typing import Dict, Any
from copy import deepcopy
import json

# ================================
# Composite
# ================================
class CompositeModule:
    def __init__(self):
        self.content = {}

    def add(self, block: dict):
        for key, value in block.items():
            if key not in self.content:
                self.content[key] = value
            else:
                if isinstance(value, dict):
                    self.content[key].update(value)

    def export(self):
        return self.content


# ================================
# Prototype Pattern
# ================================
class ResourcePrototype:
    def __init__(self, base):
        self.base = base

    def clone(self, mutator):
        copy_block = deepcopy(self.base)
        mutator(copy_block)
        return copy_block


# ================================
# NullResource Factory
# ================================
class NullResourceFactory:
    @staticmethod
    def create(name: str):
        return {
            "resource": {
                "null_resource": {
                    name: {
                        "triggers": {"dummy": "x"}
                    }
                }
            }
        }


# ================================
# InfrastructureBuilder (SIN MÓDULOS)
# ================================
class InfrastructureBuilder:
    def __init__(self):
        self.module = CompositeModule()

    def build_group(self, name: str, size: int):
        base = NullResourceFactory.create(name)
        proto = ResourcePrototype(base)

        for i in range(size):
            def mut(block, i=i):
                res = block["resource"]["null_resource"].pop(name)
                block["resource"]["null_resource"][f"{name}_{i}"] = res

            self.module.add(proto.clone(mut))

        return self

    def build(self):
        return self.module.export()


# ================================
# EJECUCIÓN
# ================================
builder = InfrastructureBuilder()
out = builder.build_group("grupo", 3).build()

print(json.dumps(out, indent=2))

with open("main.tf.json", "w") as f:
    json.dump(out, f, indent=2)
