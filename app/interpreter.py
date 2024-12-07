from app.tokens import Token
from app.tokens import TokenType

from app.runtime import MyRuntimeError
from app.expression import *
from app.statement import *
from app.environment import Environment



# Referred to as Interpreter in the book 
class Interpreter(Expr.Visitor, Stmt.Visitor):
    def __init__(self, lox):
        self._lox = lox
        self.environment = Environment()

    # LEGACY CODE 
    # def interpret(self, expr: Expr):
    #     try: 
    #         val = self.evaluate(expr)
    #         print(self.string(val))
    #     except MyRuntimeError as e:
    #         self._lox.runtimeError(e)

    def interpret(self, statements: list[Stmt]):
        # print("Interpreting:", statements[0].expression)
        try:
            for stmt in statements:
                self.execute(stmt)
        except MyRuntimeError as e:
            self._lox.runtimeError(e) 

    def execute(self, stmt: Stmt):
        # print(f"Executing {stmt}")    # DEBUG
        stmt.accept(self)

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
        return self.environment.get(expr.name)

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


    # STATE
    # Methods of the Evaluator class, as it inherits from the Visitor suite 
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
    
    def visitAssignExpr(self, expr):
        val = self.evaluate(expr.val)
        self.environment.assign

    def visitBlockStmt(self, stmt: StmtBlock) -> None:
        self.executeBlock(stmt.statements, Environment(self.environment))
        return None
    
