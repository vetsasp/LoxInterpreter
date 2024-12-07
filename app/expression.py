from abc import ABC, abstractmethod

from app.tokens import Token
from app.statement import Stmt



class Expr(Stmt, ABC):
    class Visitor(ABC):
        @abstractmethod
        def visitLiteralExpr(self, expr): 
            pass

        @abstractmethod
        def visitUnaryExpr(self, expr): 
            pass

        @abstractmethod
        def visitGroupingExpr(self, expr): 
            pass

        @abstractmethod
        def visitBinaryExpr(self, expr): 
            pass

        @abstractmethod
        def visitVariableExpr(self, expr):
            pass 

        @abstractmethod
        def visitAssignExpr(self, expr):
            pass

    @abstractmethod
    def __str__(self): 
        pass 

    @abstractmethod
    def accept(self, visitor: Visitor):
        pass

class ExprLiteral(Expr):
    def __init__(self, val):
        self.val = val
    
    def __str__(self): 
        if isinstance(self.val, bool):
            return str(self.val).lower()
        if self.val == None:
            return "nil"
        return str(self.val)
    
    def accept(self, visitor):
        return visitor.visitLiteralExpr(self)
    
class ExprUnary(Expr): 
    def __init__(self, op, expr: Expr):
        self.op = op
        self.expr = expr
    
    def __str__(self):
        return f"({self.op.lex} {self.expr})"
    
    def accept(self, visitor):
        return visitor.visitUnaryExpr(self)

class ExprGrouping(Expr): 
    def __init__(self, expr: Expr):
        self.expr = expr
    
    def __str__(self):
        return f"(group {self.expr})"
    
    def accept(self, visitor):
        return visitor.visitGroupingExpr(self)

class ExprBinary(Expr): 
    def __init__(self, op, left = None, right = None):
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.op.lex} {self.left} {self.right})"
    
    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)
    
class ExprVariable(Expr):
    def __init__(self, name: Token):
        self.name = name

    def __str__(self):
        return f"{self.name.lex}"   # TODO 
    
    def accept(self, visitor):
        return visitor.visitVariableExpr(self)
    
class ExprAssign(Expr):
    def __init__(self, name: Token, val: Expr):
        self.name = name
        self.val = val
        
    def accept(self, visitor):
        return visitor.visitAssignExpr(self)