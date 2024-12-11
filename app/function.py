from app.callable import LoxCallable
from app.environment import Environment
from app.statement import StmtFunction
from app.ret import ReturnExcept 


class LoxFunction(LoxCallable):
    def __init__(self, declaration, closure: Environment, isInit: bool): 
        self.declaration = declaration
        self.closure = closure
        self.isInit = isInit

    def call(self, interpreter, args) -> None:
        env: Environment = Environment(self.closure)

        for i, v in enumerate(self.declaration.params):
            env.define(v.lex, args[i])

        try: 
            interpreter.executeBlock(self.declaration.body, env)
        except ReturnExcept as ret:
            if self.isInit:
                return self.closure.getAt(0, "this")
            return ret.val

        if self.isInit:
            return self.closure.getAt(0, "this")
        return None 
    
    def arity(self) -> int:
        return len(self.declaration.params)
    
    def __str__(self) -> str: 
        return f"<fn {self.declaration.name.lex}>"
    
    def bind(self, instance):
        env = Environment(self.closure)
        env.define("this", instance)
        return LoxFunction(self.declaration, env, self.isInit)