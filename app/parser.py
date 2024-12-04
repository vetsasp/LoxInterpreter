from app.tokens import TokenType
from app.tokens import Token
from app.expression import *
# from app.statement import Stmt 


class Parser:
    class ParseError(Exception):
        def __init__(self, token, msg):
            self.token = token
            self.msg = msg

    # Parser init 
    def __init__(self, lox, tokens: list[Token]):
        self._lox = lox
        self._tokens = tokens
        self.head = None 
        self._pos = 0

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
        return self.peek().type == t

    def match(self, *types) -> bool:
        for t in types:
            if self.check(t):
                self.advance()
                return True
        return False
    
    def consume(self, t: TokenType, msg: str) -> Token:
        if self.check(t):
            return self.advance()
        
        raise self.error(self.peek(), msg)
    
    def error(self, token: Token, msg: str) -> ParseError:
        self._lox.parseError(token, msg)
        return self.ParseError(token, msg)
    
    # for use with statements
    def sync(self) -> None:
        self.advance()

        while not self.atEnd():
            if self.prev().type == TokenType.SEMICOLON:
                return
            
            # set of tokens that can start a statement
            st = [
                TokenType.CLASS, TokenType.FUN, TokenType.VAR, TokenType.FOR, \
                TokenType.IF, TokenType.WHILE, TokenType.PRINT, TokenType.RETURN
            ]

            if self.peek().type in st:
                return

            self.advance()






    # The Grammar 
    def expression(self) -> Expr:
        return self.equality()

    def equality(self) -> Expr:
        expr = self.comparison()

        # match !=, ==
        while (self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL)):
            op: Token = self.prev()
            right: Expr = self.comparison()
            expr = Binary(op, expr, right)

        return expr

    def comparison(self) -> Expr:
        expr: Expr = self.term() 

        # match >, >=, <, <=
        while (self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, \
                          TokenType.LESS, TokenType.LESS_EQUAL)):
            op: Token = self.prev()
            right: Expr = self.term()
            expr = Binary(op, expr, right)
        
        return expr 

    def term(self) -> Expr:
        expr: Expr = self.factor()

        # match +, -
        while (self.match(TokenType.MINUS, TokenType.PLUS)):
            op: Token = self.prev()
            right: Expr = self.factor()
            expr = Binary(op, expr, right)

        return expr

    def factor(self) -> Expr:
        expr: Expr = self.unary()

        # match /, *
        while (self.match(TokenType.SLASH, TokenType.STAR)):
            op: Token = self.prev()
            right: Expr = self.unary()
            expr = Binary(op, expr, right)

        return expr 

    def unary(self) -> Expr:
        # match !, -
        if self.match(TokenType.BANG, TokenType.MINUS):
            op: Token = self.prev()
            right: Expr = self.unary()
            return Unary(op, right)
        
        return self.primary()

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return Literal(False)
        if self.match(TokenType.TRUE):
            return Literal(True)
        if self.match(TokenType.NIL):
            return Literal(None)
        
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.prev().lit)
        
        # match ( expr )
        if self.match(TokenType.LEFT_PAREN):
            expr: Expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Grouping(expr)
        
        # if expr falls thru, raise error
        raise self.error(self.peek(), "Expected expression.")



    # Legacy code
    def parse(self):
        try:
            return self.expression()
        except self.ParseError as e:
            return None




''' INTRODUCTION OF STATEMENTS
    def statement(self) -> Stmt:
        if self.match(TokenType.PRINT):
            return self.printStatement()
        return self.expressionStatement()

    def printStatement(self) -> Stmt:
        val = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Stmt.Print(val)

    def expressionStatement(self) -> Stmt:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Stmt.Expression(expr)

    def parse(self): 
        statements = []
        while not self.atEnd():
            statements.append(self.statement())
        return statements
    

'''
    #