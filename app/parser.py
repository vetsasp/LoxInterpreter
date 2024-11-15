from app.tokens import TokenType
from app.tokens import Token

from abc import ABC, abstractmethod

class Expr(ABC):
    @abstractmethod
    def __str__(self): 
        pass 

class Literal(Expr):
    def __init__(self, val):
        self.val = val
    
    def __str__(self): 
        return str(self.val)
    
class Unary(Expr): 
    def __init__(self, op, expr: super = None):
        self.op = op
        self.expr = expr
    
    def __str__(self):
        return f"({self.op.lex} {self.expr})"

class Grouping(Expr): 
    def __init__(self, expr: super = None):
        self.expr = expr
    
    def __str__(self):
        return f"(group {self.expr})"

class Binary(Expr): 
    def __init__(self, op, left = None, right = None):
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.op.lex} {self.left} {self.right})"



class Parser:
    # Parser init 
    def __init__(self, tokens: list[Token]):
        self._tokens = tokens
        self.head = None 
        self._pos = 0

    def printTree(self) -> None: 
        print(self.head)

    # functions from the book 
    def atEnd(self) -> bool:
        if self._pos >= len(self._tokens) - 1:
            return True
        return False 

    def prev(self) -> Token:
        return self._tokens[self._pos - 1]

    def advance(self) -> Token:
        if not self.atEnd():
            self._pos += 1
        return self.prev()
    
    def peek(self) -> Token: 
        return self._tokens[self._pos] 

    def check(self, t: TokenType) -> bool:
        if self.atEnd():
            return False
        return self.peek().token_type == t

    def match(self, *types) -> bool:
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False
    
    def consume(self, t: TokenType, msg: str) -> Token:
        if self.check(t):
            return self.advance()
        
        raise ValueError(f"Error: {msg} at {self.peek()}")
    

    # The Grammar 
    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()

        while (self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL)):
            op: Token = self.prev()
            right: Expr = self.comparison()
            expr = Binary(op, expr, right)

        return expr

    def comparison(self) -> Expr:
        expr: Expr = self.term() 

        while (self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL)):
            op: Token = self.prev()
            right: Expr = self.term()
            expr = Binary(op, expr, right)
        
        return expr 

    def term(self) -> Expr:
        expr: Expr = self.factor()

        while (self.match(TokenType.MINUS, TokenType.PLUS)):
            op: Token = self.prev()
            right: Expr = self.factor()
            expr = Binary(op, expr, right)

        return expr

    def factor(self) -> Expr:
        expr: Expr = self.unary()

        while (self.match(TokenType.SLASH, TokenType.STAR)):
            op: Token = self.prev()
            right: Expr = self.unary()
            expr = Binary(op, expr, right)

        return expr 

    def unary(self) -> Expr:
        if self.match(TokenType.BANG, TokenType.MINUS):
            op: Token = self.prev()
            right: Expr = self.unary()
            return Unary(op, right)
        
        return self.primary()

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return Literal("false")
        if self.match(TokenType.TRUE):
            return Literal("true")
        if self.match(TokenType.NIL):
            return Literal("nil")
        
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.prev().lit)
        
        if self.match(TokenType.LEFT_PAREN):
            expr: Expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)

    def parse(self) -> None:
        self.head = self.expression()
