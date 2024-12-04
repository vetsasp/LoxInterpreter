from app.tokens import Token

class MyRuntimeError(Exception): 
    def __init__(self, token: Token, msg: str):
        super().__init__(msg)
        self.token = token 
        self.msg = msg
    
    def __str__(self):
        return f"{self.msg}\n[line {self.token.line}]"