from enum import Enum

from app.tokens import Token
from app.statement import *
from app.expression import *
from app.interpreter import Interpreter



class Resolver(Expr.Visitor, Stmt.Visitor):
    
    class FunctionType(Enum):
        NONE = 0, 
        FUNCTION = 1,
        INITIALIZER = 2,
        METHOD = 3

    class ClassType(Enum):
        NONE = 0,
        CLASS = 1,
        SUBCLASS = 2

    currentClass: ClassType = ClassType.NONE

    def __init__(self, interpreter):
        self.interpreter: Interpreter = interpreter 
        self.scopes: list[dict[str, bool]] = []
        self.currentFunction = self.FunctionType.NONE
        self.currentClass: self.ClassType = self.ClassType.NONE

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
            self.interpreter.lox.parseError(name, "Already a variable with this name in this scope.")

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
        enclosingFunction: Resolver.FunctionType = self.currentFunction
        self.currentFunction = t
        self.beginScope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolve(function.body)
        self.endScope()
        self.currentFunction = enclosingFunction


    # Visit Expressions 
    def visitVariableExpr(self, expr: ExprVariable) -> None:
        if self.scopes and self.peek().get(expr.name.lex) == False:
            self.interpreter.lox.parseError(expr.name, \
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

    def visitGetExpr(self, expr: ExprGet) -> None:
        self.resolve(expr.obj)

    def visitSetExpr(self, expr: ExprSet) -> None:
        self.resolve(expr.val)
        self.resolve(expr.obj)

    def visitThisExpr(self, expr: ExprThis) -> None:
        if self.currentClass == self.ClassType.NONE:
            self.interpreter.lox.parseError(expr.keyword, \
                "Can't use 'this' outside of a class.")
            return 
        self.resolveLocal(expr, expr.keyword)

    def visitSuperExpr(self, expr: ExprSuper) -> None:
        if self.currentClass == self.ClassType.NONE:
            self.interpreter.lox.parseError(expr.keyword, \
                "Can't use 'super' outside of a class.")
        elif self.currentClass != self.ClassType.SUBCLASS:
            self.interpreter.lox.parseError(expr.keyword, \
                "Can't use 'super' in a class with no superclass.")
            
        self.resolveLocal(expr, expr.keyword)
        



    # Visit Statements 
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
        self.resolveFunction(stmt, self.FunctionType.FUNCTION)
    
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
        if self.currentFunction == self.FunctionType.NONE:
            self.interpreter.lox.parseError(stmt.keyword, \
                                       "Can't return from top-level code.")
        if stmt.value:
            if self.currentFunction == self.FunctionType.INITIALIZER:
                self.interpreter.lox.parseError(stmt.keyword, \
                    "Can't return a value from an initializer.")
            self.resolve(stmt.value)
    
    def visitWhileStmt(self, stmt: StmtWhile) -> None:
        self.resolve(stmt.condition)
        self.resolve(stmt.body)
    
    def visitClassStmt(self, stmt: StmtClass) -> None: 
        enclosingClass: Resolver.ClassType = self.currentClass
        self.currentClass = self.ClassType.CLASS

        self.declare(stmt.name)
        self.define(stmt.name)

        if stmt.superclass:
            if stmt.name.lex == stmt.superclass.name.lex:
                self.interpreter.lox.parseError(stmt.superclass.name, \
                    "A class can't inherit from itself.")
            self.currentClass = self.currentClass.SUBCLASS
            self.resolve(stmt.superclass)

        if stmt.superclass:
            self.beginScope()
            self.peek()["super"] = True

        self.beginScope()
        self.peek()["this"] = True 

        for method in stmt.methods:
            declaration = self.FunctionType.METHOD if \
                method.name.lex == "init" else self.FunctionType.INITIALIZER
            self.resolveFunction(method, declaration)
        
        self.endScope()

        if stmt.superclass:
            self.endScope()

        self.currentClass = enclosingClass