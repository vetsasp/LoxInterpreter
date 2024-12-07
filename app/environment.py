from app.tokens import Token
from app.runtime import MyRuntimeError



class Environment:
    def __init__(self, env = None):
        self._values = {}
        self.enclosing: Environment = env

    def define(self, name: str, val):
        self._values[name] = val 

    def get(self, name: Token):
        print("Getting:", name)
        l = name.lex
        if l in self._values:
            return self._values[l]
        
        if self.enclosing is not None:
            return self.enclosing.get(name) 

        raise MyRuntimeError(name, f"Undefined variable '{l}'.")
    
    def assign(self, name: Token, val):
        if name.lex in self._values:
            self._values[name.lex] = val
            return

        if self.enclosing is not None:
            self.enclosing.assign(name, val)
            return 
        
        raise MyRuntimeError(name, f"Undefined variable '{name.lex}'.")