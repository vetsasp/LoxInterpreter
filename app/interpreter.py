from app.tokens import Token
from app.tokens import TokenType

from app.runtime import MyRuntimeError
from app.expression import *
from app.statement import *
from app.environment import Environment
from app.callable import LoxCallable
from app.function import LoxFunction
from app.ret import ReturnExcept
from app.loxclass import LoxClass
from app.instance import LoxInstance



# Referred to as Interpreter in the book 
class Interpreter(Expr.Visitor, Stmt.Visitor):
    def __init__(self, lox):
        self.lox = lox
        self.globals = Environment()
        self.environment = self.globals 
        self.locals: dict[Expr, int] = {}

        class Clock(LoxCallable):
            def arity(self) -> int:
                return 0
            
            def call(self, interpreter, args):
                import time
                return time.time()
            
            def __str__(self) -> str:
                return "<native fn>"
            
        self.globals.define("clock", Clock())

    # LEGACY CODE 
    # Needed to pass evaluate cmd test cases
    def evaluate_LEGACY(self, expr):
        try:
            val = self.evaluate(expr.expression)
            print(self.string(val))
        except MyRuntimeError as e:
            self.lox.runtimeError(e)

    def interpret(self, statements: list[Stmt]):
        try:
            for stmt in statements:
                self.execute(stmt)
        except MyRuntimeError as e:
            self.lox.runtimeError(e) 

    def execute(self, stmt: Stmt):
        stmt.accept(self)

    def resolve(self, expr: Expr, depth: int) -> None:
        self.locals[expr] = depth 

    def executeBlock(self, statements: list[Stmt], env: Environment):
        prev: Environment = self.environment

        try:
            self.environment = env 

            for stmt in statements:
                self.execute(stmt)
        
        finally: 
            self.environment = prev 

    @staticmethod
    def string(s) -> str:
        # aesthetic fixes 
        if isinstance(s, float) and s.is_integer():
            return str(int(s))
        if isinstance(s, bool):
            return "true" if s else "false"
        if s == None:
            return "nil"
        return s

    def evaluate(self, expr: Expr): 
        return expr.accept(self)

    def visitLiteralExpr(self, expr: ExprLiteral): 
        return expr.val 

    def visitUnaryExpr(self, expr: ExprUnary): 
        child = self.evaluate(expr.expr)

        if expr.op.type == TokenType.BANG:
            return not self.isTruthful(child)
        elif expr.op.type == TokenType.MINUS:
            self.checkNumberOperand(expr.op, child)
            return -child
        
        print("unary evaluate failed")

    def visitGroupingExpr(self, expr: ExprGrouping): 
        return self.evaluate(expr.expr)

    def visitBinaryExpr(self, expr: ExprBinary): 
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        t = expr.op.type 

        if t == TokenType.GREATER:
            self.checkNumberOperands(expr.op, left, right)
            return left > right 
        elif t == TokenType.GREATER_EQUAL:
            self.checkNumberOperands(expr.op, left, right)
            return left >= right 
        elif t == TokenType.LESS:
            self.checkNumberOperands(expr.op, left, right)
            return left < right 
        elif t == TokenType.LESS_EQUAL:
            self.checkNumberOperands(expr.op, left, right)
            return left <= right 
        elif t == TokenType.BANG_EQUAL:
            return not left == right 
        elif t == TokenType.EQUAL_EQUAL:
            return left == right 
        elif t == TokenType.MINUS:
            self.checkNumberOperands(expr.op, left, right)
            return left - right
        elif t == TokenType.PLUS:
            self.checkPlusOperands(expr.op, left, right)
            return left + right 
        elif t == TokenType.SLASH:
            self.checkNumberOperands(expr.op, left, right)
            return left / right 
        elif t == TokenType.STAR:
            self.checkNumberOperands(expr.op, left, right)
            return left * right 
        
        print("binary evaluate failed")

    # New Expressions 
    def visitVariableExpr(self, expr: ExprVariable):
        return self.lookupVariable(expr.name, expr)
        # return self._environment.get(expr.name)   # LEGACY

    @staticmethod
    def isTruthful(obj) -> bool:
        if obj == None:
            return False
        if isinstance(obj, bool):
            return obj
        return True

    @staticmethod
    def checkNumberOperand(operator: Token, operand):
        if isinstance(operand, float):
            return
        raise MyRuntimeError(operator, "Operand must be a number.")

    @staticmethod
    def checkNumberOperands(operator: Token, *operands):
        for operand in operands:
            if not isinstance(operand, float):
                raise MyRuntimeError(operator, "Operands must be numbers.")
        return 

    @staticmethod
    def checkPlusOperands(operator: Token, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return
        if isinstance(left, str) and isinstance(right, str):
            return
        raise MyRuntimeError(operator, "Operands must be two numbers or two strings.")


    def lookupVariable(self, name: Token, expr: Expr):
        dist = self.locals.get(expr)
        if dist is not None:
            return self.environment.getAt(dist, name.lex)
        else:
            return self.globals.get(name)

    # STATE
    # Methods of the Evaluator class, as it inherits from the Visitor suite 


    # Exprs 
    def visitCallExpr(self, expr: ExprCall):
        callee = self.evaluate(expr.callee)
        args = [self.evaluate(arg) for arg in expr.args]

        if not isinstance(callee, LoxCallable):
            raise MyRuntimeError(expr.paren, \
                "Can only call functions and classes.")
        
        if len(args) != callee.arity():
            raise MyRuntimeError(expr.paren, \
                f"Expected {callee.arity()} arguments but got {len(args)}.")

        return callee.call(self, args) 
    
    # def visitAssignExpr(self, expr):
    #     val = self.evaluate(expr.val)
    #     self._environment.assign(expr.name, val)
    #     return val

    def visitAssignExpr(self, expr):
        val = self.evaluate(expr.val)

        dist: int = self.locals.get(expr)
        if dist is not None:
            self.environment.assignAt(dist, expr.name, val)
        else:
            self.globals.assign(expr.name, val)

        return val

    def visitLogicalExpr(self, expr):
        left = self.evaluate(expr.left)

        if expr.op.type == TokenType.OR:
            # if OR and left is truthful
            if self.isTruthful(left):
                return left
        elif not self.isTruthful(left):
            # if AND and left is NOT truthful
            return left 
        
        # if OR and left was NOT truthful | AND and left was truthful
        # Only evaluate the right side IF there was reason to do so 
        return self.evaluate(expr.right) 
    
    def visitGetExpr(self, expr: ExprGet):
        obj = self.evaluate(expr.obj)
        if isinstance(obj, LoxInstance):
            return obj.get(expr.name)
        
        raise MyRuntimeError(expr.name, "Only instances have properties.")
    
    def visitSetExpr(self, expr: ExprSet):
        obj = self.evaluate(expr.obj)
        if not isinstance(obj, LoxInstance):
            raise MyRuntimeError(expr.name, "Only instances have fields.")
        
        val = self.evaluate(expr.val)
        obj.set(expr.name, val)
        return val
    
    def visitThisExpr(self, expr: ExprThis):
        return self.lookupVariable(expr.keyword, expr)
    
    def visitSuperExpr(self, expr: ExprSuper):
        dist = self.locals.get(expr)
        superclass: LoxClass = self.environment.getAt(dist, "super")

        obj: LoxInstance = self.environment.getAt(dist - 1, "this")

        method: LoxFunction = superclass.findMethod(expr.method.lex)

        if method is None:
            raise MyRuntimeError(expr.method, \
                "Undefined property '" + expr.method.lex + "'.")
        
        return method.bind(obj) 

    # Stmts
    def visitReturnStmt(self, stmt: StmtReturn):
        val = None 
        if stmt.value != None:
            val = self.evaluate(stmt.value)
        
        raise ReturnExcept(val) 

    def visitFunctionStmt(self, stmt) -> None:
        function: LoxFunction = LoxFunction(stmt, self.environment, False)
        self.environment.define(stmt.name.lex, function)
        return None
    
    def visitIfStmt(self, stmt: StmtIf) -> None:
        if (self.isTruthful(self.evaluate(stmt.condition))):
            self.execute(stmt.thenBranch)
        elif stmt.elseBranch is not None:
            self.execute(stmt.elseBranch)
        return None

    def visitBlockStmt(self, stmt: StmtBlock) -> None:
        self.executeBlock(stmt.statements, Environment(self.environment))
        return None
    
    def visitWhileStmt(self, stmt):
        while self.isTruthful(self.evaluate(stmt.condition)):
            self.execute(stmt.body)
        return None 
    
    def visitExpressionStmt(self, stmt: StmtExpression) -> None:
        self.evaluate(stmt.expression)
        return None

    def visitPrintStmt(self, stmt: StmtPrint) -> None:
        val = self.evaluate(stmt.expression)
        print(self.string(val))
        return None 
    
    def visitVarStmt(self, stmt: StmtVariable) -> None:
        val = None
        if stmt.initializer != None:
            val = self.evaluate(stmt.initializer)

        self.environment.define(stmt.name.lex, val)
        return None 
    
    def visitClassStmt(self, stmt: StmtClass) -> None:
        superclass = None
        if stmt.superclass:
            superclass = self.evaluate(stmt.superclass)
            if not isinstance(superclass, LoxClass):
                raise MyRuntimeError(stmt.superclass.name, \
                    "Superclass must be a class.")
            
        self.environment.define(stmt.name.lex, None)
        # clss: LoxClass = LoxClass(stmt.name.lex) # LEGACY 

        if stmt.superclass:
            self.environment = Environment(self.environment)
            self.environment.define("super", superclass)

        methods: dict[str, LoxFunction] = {}
        for method in stmt.methods:
            func: LoxFunction = LoxFunction(method, self.environment, \
                                            method.name.lex == "init")
            methods[method.name.lex] = func  

        clss: LoxClass = LoxClass(stmt.name.lex, superclass, methods) 

        if superclass:
            self.environment = self.environment.enclosing

        self.environment.assign(stmt.name, clss)