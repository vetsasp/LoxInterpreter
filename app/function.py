from app.callable import LoxCallable
from app.environment import Environment
from app.statement import StmtFunction
from app.ret import ReturnExcept 


class LoxFunction(LoxCallable):
    def __init__(self, declaration): 
        self.declaration = declaration

    def call(self, interpreter, args) -> None:
        env: Environment = Environment(interpreter.globals)

        for i, v in enumerate(self.declaration.params):
            env.define(v.lex, args[i])

        try: 
            interpreter.executeBlock(self.declaration.body, env)
        except ReturnExcept as ret:
            return ret.val

        return None 
    
    def arity(self) -> int:
        return len(self.declaration.params)
    
    def __str__(self) -> str: 
        return f"<fn {self.declaration.name.lex}>"