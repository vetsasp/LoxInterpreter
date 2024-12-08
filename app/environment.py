from app.tokens import Token
from app.runtime import MyRuntimeError



class Environment:
    def __init__(self, env = None):
        self._values = {}
        self.enclosing: Environment = env

    def define(self, name: str, val):
        self._values[name] = val 

    def ancestor(self, dist: int):
        env: Environment = self
        for i in range(dist):
            env = env.enclosing
        return env 
    
    def getAt(self, dist: int, name: str):
        return self.ancestor(dist)._values.get(name)

    def get(self, name: Token):
        l = name.lex
        if l in self._values:
            return self._values[l]
        
        if self.enclosing is not None:
            return self.enclosing.get(name) 

        raise MyRuntimeError(name, f"Undefined variable '{l}'.")
    
    def assignAt(self, dist: int, name: Token, val) -> None:
        self.ancestor(dist)._values[name.lex] = val

    def assign(self, name: Token, val):
        if name.lex in self._values:
            self._values[name.lex] = val
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, val)
            return 
        
        raise MyRuntimeError(name, f"Undefined variable '{name.lex}'.")