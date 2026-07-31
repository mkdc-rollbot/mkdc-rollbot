from dataclasses import dataclass

@dataclass
class EngineRegistration:
    ruleset: str
    url: str
    healthy: bool = True

class Registry:
    def __init__(self):
        self._engines = {}

    def register(self, engine: EngineRegistration):
        self._engines[engine.ruleset] = engine

    def resolve(self, ruleset):
        return self._engines[ruleset]
