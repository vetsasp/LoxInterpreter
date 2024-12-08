from enum import Enum

from app.tokens import Token
from app.statement import *
from app.expression import *
from app.interpreter import Interpreter


class FunctionType(Enum):
    NONE = 1, 
    FUNCTION = 2


class Resolver(Expr.Visitor, Stmt.Visitor):
    def __init__(self, interpreter):
        self.interpreter: Interpreter = interpreter 
        self.scopes: list[dict[str, bool]] = []
        self.currentFunction = FunctionType.NONE

    def peek(self) -> dict[str, bool]:
        return self.scopes[-1]

    # Universal resolver
    def resolve(self, inp) -> None:
        if isinstance(inp, list):
            for stmt in inp:
                if not isinstance(stmt, Stmt):
                    print("Resolver@resolve: inp is not list[Stmt]")
                self.resolve(stmt)
        elif isinstance(inp, Stmt):
            inp.accept(self)
        elif isinstance(inp, Expr):
            inp.accept(self)
    
    '''
        The problem with this is that Python does not have function overloading
        These must be handled by 1 function, or become 3 separate functions 

        def resolve(self, stmts: list[Stmt]) -> None:
            for stmt in stmts:
                self.resolve(stmt)

        def resolve(self, stmt: Stmt):
            stmt.accpet(self)

        def resolve(self, expr: Expr):
            expr.accept(self)
    '''

    def beginScope(self) -> None:
        self.scopes.append({}) 

    def endScope(self) -> None:
        self.scopes.pop()

    def declare(self, name: Token) -> None:
        if not self.scopes: # if scopes is empty 
            return 
        
        scope: dict[str, bool] = self.peek()

        if name.lex in scope:
            self.interpreter.lox.error(name, "Already a variable with this name in this scope.")

        scope[name.lex] = False 
    
    def define(self, name: Token) -> None:
        if not self.scopes:
            return
        (self.peek())[name.lex] = True 

    def resolveLocal(self, expr: Expr, name: Token) -> None:
        for i in range(len(self.scopes) - 1, -1, -1):
            if name.lex in self.scopes[i]:
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return
            
    def resolveFunction(self, function: StmtFunction, t: FunctionType) -> None:
        enclosingFunction: FunctionType = self.currentFunction
        self.currentFunction = t
        self.beginScope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.endScope()
        self.currentFunction = enclosingFunction
        
    def visitBlockStmt(self, stmt: StmtBlock) -> None:
        self.beginScope()
        self.resolve(stmt.statements)
        self.endScope()
    
    def visitVarStmt(self, stmt: StmtVariable) -> None:
        self.declare(stmt.name)
        if stmt.initializer:
            self.resolve(stmt.initializer)
        
        self.define(stmt.name)
    
    def visitFunctionStmt(self, stmt: StmtFunction) -> None:
        self.declare(stmt.name)
        self.define(stmt.name)
        self.resolveFunction(stmt, FunctionType.FUNCTION)
    
    def visitExpressionStmt(self, stmt: StmtExpression) -> None:
        self.resolve(stmt.expression)
    
    def visitIfStmt(self, stmt: StmtIf) -> None:
        self.resolve(stmt.condition)
        self.resolve(stmt.thenBranch)
        if stmt.elseBranch:
            self.resolve(stmt.elseBranch)
    
    def visitPrintStmt(self, stmt: StmtPrint) -> None:
        self.resolve(stmt.expression)
    
    def visitReturnStmt(self, stmt: StmtReturn) -> None:
        if self.currentFunction == FunctionType.NONE:
            self.interpreter.lox.error(stmt.keyword, "Can't return from top-level code.")
        if stmt.value:
            self.resolve(stmt.value)
    
    def visitWhileStmt(self, stmt: StmtWhile) -> None:
        self.resolve(stmt.condition)
        self.resolve(stmt.body)
    
    def visitVariableExpr(self, expr: ExprVariable) -> None:
        if self.scopes and self.peek().get(expr.name.lex) == False:
            self.interpreter.lox.error(expr.name, \
                      "Can't read local variable in its own initializer.")
            
        self.resolveLocal(expr, expr.name)
    
    def visitAssignExpr(self, expr: ExprAssign) -> None:
        self.resolve(expr.val)
        self.resolveLocal(expr, expr.name)
    
    def visitBinaryExpr(self, expr: ExprBinary) -> None:
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visitCallExpr(self, expr: ExprCall) -> None:
        self.resolve(expr.callee)
        for arg in expr.args:
            self.resolve(arg)
    
    def visitGroupingExpr(self, expr: ExprGrouping) -> None:
        self.resolve(expr.expr)
    
    def visitLiteralExpr(self, expr: ExprLiteral) -> None:
        self.resolve(expr.val)
    
    def visitLogicalExpr(self, expr: ExprLogical) -> None:
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visitUnaryExpr(self, expr: ExprUnary) -> None:
        self.resolve(expr.expr)