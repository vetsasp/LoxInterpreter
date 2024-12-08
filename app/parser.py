from app.tokens import TokenType
from app.tokens import Token
from app.expression import *
from app.statement import *


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
        
        if self._lox.ignore_error and t == TokenType.SEMICOLON:
            return
        
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
        return self.assignment()
        # return self.equality()    # LEGACY

    def assignment(self):
        expr: Expr = self.orOp()

        if self.match(TokenType.EQUAL):
            equals: Token = self.prev()
            val: Expr = self.assignment()

            if isinstance(expr, ExprVariable):
                name: Token = expr.name
                return ExprAssign(name, val)
            
            self.error(equals, "Invalid assignment target.")
            
        return expr 
    
    def orOp(self) -> Expr:
        expr: Expr = self.andOp()

        while self.match(TokenType.OR):
            op: Token = self.prev()
            right: Expr = self.andOp()
            expr = ExprLogical(expr, op, right)
        return expr 
    
    def andOp(self) -> Expr:
        expr: Expr = self.equality()

        while self.match(TokenType.AND):
            op: Token = self.prev()
            right: Expr = self.equality()
            expr = ExprLogical(expr, op, right)
        return expr     

    def equality(self) -> Expr:
        expr = self.comparison()

        # match !=, ==
        while (self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL)):
            op: Token = self.prev()
            right: Expr = self.comparison()
            expr = ExprBinary(op, expr, right)

        return expr

    def comparison(self) -> Expr:
        expr: Expr = self.term() 

        # match >, >=, <, <=
        while (self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, \
                          TokenType.LESS, TokenType.LESS_EQUAL)):
            op: Token = self.prev()
            right: Expr = self.term()
            expr = ExprBinary(op, expr, right)
        
        return expr 

    def term(self) -> Expr:
        expr: Expr = self.factor()

        # match +, -
        while (self.match(TokenType.MINUS, TokenType.PLUS)):
            op: Token = self.prev()
            right: Expr = self.factor()
            expr = ExprBinary(op, expr, right)

        return expr

    def factor(self) -> Expr:
        expr: Expr = self.unary()

        # match /, *
        while (self.match(TokenType.SLASH, TokenType.STAR)):
            op: Token = self.prev()
            right: Expr = self.unary()
            expr = ExprBinary(op, expr, right)

        return expr 

    def unary(self) -> Expr:
        # match !, -
        if self.match(TokenType.BANG, TokenType.MINUS):
            op: Token = self.prev()
            right: Expr = self.unary()
            return ExprUnary(op, right)
        
        return self.call()
    
    def call(self) -> Expr:
        expr: Expr = self.primary()

        while True:
            if self.match(TokenType.LEFT_PAREN):
                expr = self.finishCall(expr)
            else:
                break

        return expr
    
    def finishCall(self, callee: Expr) -> Expr:
        args: list[Expr] = []
        if not self.check(TokenType.RIGHT_PAREN):
            args.append(self.expression())
            while self.match(TokenType.COMMA):
                if len(args) >= 255:
                    self.error(self.peek(), \
                            "Can't have more than 255 arguments.")
                args.append(self.expression())
        
        paren: Token = self.consume(TokenType.RIGHT_PAREN, \
                                    "Expect ')' after arguments.")
        return ExprCall(callee, paren, args)

    def primary(self) -> Expr:
        if self.match(TokenType.FALSE):
            return ExprLiteral(False)
        if self.match(TokenType.TRUE):
            return ExprLiteral(True)
        if self.match(TokenType.NIL):
            return ExprLiteral(None)
        
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return ExprLiteral(self.prev().lit)
        
        if self.match(TokenType.IDENTIFIER):
            return ExprVariable(self.prev())
        
        # match ( expr )
        if self.match(TokenType.LEFT_PAREN):
            expr: Expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return ExprGrouping(expr)
        
        # if expr falls thru, raise error
        raise self.error(self.peek(), "Expected expression.")



    # Legacy code
    # def parse(self):
    #     try:
    #         return self.expression()
    #     except self.ParseError as e:
    #         return None




# INTRODUCTION OF STATEMENTS
    def parse(self): 
        statements: list[Stmt] = []
        while not self.atEnd():
            # print("Parsing loop...")    # DEBUG
            statements.append(self.declaration())
        return statements
    
    def declaration(self):
        try:
            if self.match(TokenType.FUN):
                return self.function("function")
            if self.match(TokenType.VAR):
                return self.varDeclaration()
            return self.statement()
        except self.ParseError as e:
            self.sync()
            return None 
        
    def varDeclaration(self) -> Stmt:
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

        init = None 
        if self.match(TokenType.EQUAL):
            init = self.expression()
        
        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return StmtVariable(name, init)
    
    def statement(self) -> Stmt:
        if self.match(TokenType.FOR):
            return self.forStatement()
        
        if self.match(TokenType.IF):
            return self.ifStatement()

        if self.match(TokenType.PRINT):
            return self.printStatement()
        
        if self.match(TokenType.WHILE):
            return self.whileStatement()

        if self.match(TokenType.LEFT_BRACE):\
            return StmtBlock(self.block())

        return self.expressionStatement()
    
    def forStatement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        initializer = None

        if self.match(TokenType.SEMICOLON):
            initializer = None
        elif self.match(TokenType.VAR):
            initializer = self.varDeclaration()
        else:
            initializer = self.expressionStatement()

        cond = None 

        if not self.check(TokenType.SEMICOLON):
            cond = self.expression()
        
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        inc = None 

        if not self.check(TokenType.RIGHT_PAREN):
            inc = self.expression()
        
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body: Stmt = self.statement()

        if inc is not None: 
            body = StmtBlock([body, StmtExpression(inc)])
        
        if cond is None:
            cond = ExprLiteral(True)
        
        body = StmtWhile(cond, body) 

        if initializer is not None: 
            body = StmtBlock([initializer, body])

        return body

    def ifStatement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        cond: Expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        thenBranch: Stmt = self.statement()
        elseBranch: Stmt = None
        if self.match(TokenType.ELSE):
            elseBranch = self.statement()
        
        return StmtIf(cond, thenBranch, elseBranch)
        

    def printStatement(self) -> Stmt:
        val = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return StmtPrint(val)
    
    def whileStatement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        cond: Expr = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body: Stmt = self.statement()

        return StmtWhile(cond, body)

    def expressionStatement(self) -> Stmt:
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return StmtExpression(expr)

    def returnStatement(self) -> Stmt:
        keyword: Token = self.prev()
        val = None
        if not self.check(TokenType.SEMICOLON):
            val = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return StmtReturn(keyword, val)

    def block(self):
        statements: list[Stmt] = []

        while not self.check(TokenType.RIGHT_BRACE) and \
                not self.atEnd():
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        return statements

    def function(self, kind: str) -> StmtFunction: 
        name: Token = self.consume(TokenType.IDENTIFIER, \
                                   f"Expect {kind} name.")
        
        self.consume(TokenType.LEFT_PAREN, f"Expect '(' after {kind} name.")
        params: list[Token] = []
        if not self.check(TokenType.RIGHT_PAREN):
            if len(params) >= 255:
                self.error(self.peek(), \
                           "Can't have more than 255 parameters.")
            params.append(
                self.consume(TokenType.IDENTIFIER, "Expect parameter name.")
            )
            while self.match(TokenType.COMMA):
                if len(params) >= 255:
                    self.error(self.peek(), \
                            "Can't have more than 255 parameters.")
                params.append(
                    self.consume(TokenType.IDENTIFIER, "Expect parameter name.")
                )
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")

        self.consume(TokenType.LEFT_BRACE, "Expect '{' before " + kind + " body.")
        body: list[Stmt] = self.block()
        return StmtFunction(name, params, body) 