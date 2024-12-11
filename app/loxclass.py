from app.callable import LoxCallable
from app.instance import LoxInstance
from app.function import LoxFunction


class LoxClass(LoxCallable):
    def __init__(self, name: str, methods: dict[str, LoxFunction]):
        self.name = name 
        self.methods = methods 

    def __str__(self) -> str:
        return self.name 
    
    def call(self, interpreter, args):
        instance = LoxInstance(self)

        init: LoxFunction = self.findMethod("init")
        if init is not None:
            init.bind(instance).call(interpreter, args)

        return instance 
    
    def arity(self) -> int:
        init: LoxFunction = self.findMethod("init")
        if init is None:
            return 0
        return init.arity()
    
    def findMethod(self, name: str):
        if name in self.methods:
            return self.methods[name]