from app.runtime import MyRuntimeError
from app.tokens import Token
from app.function import LoxFunction



class LoxInstance:
    def __init__(self, klass):
        self.klass = klass
        self.fields: dict[str, object] = {}

    def __str__(self):
        return self.klass.name + " instance"
    
    def get(self, name: Token):
        if name.lex in self.fields:
            return self.fields[name.lex]
        
        method: LoxFunction = self.klass.findMethod(name.lex)
        if method is not None:
            return method.bind(self)

        raise MyRuntimeError(name, "Undefined property '" + name.lex + "'.")
    
    def set(self, name: Token, val):
        self.fields[name.lex] = val 