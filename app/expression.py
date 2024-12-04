from abc import ABC, abstractmethod
# from app.statement import Stmt



class Expr(ABC): #Stmt, ABC):
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
    def __str__(self): 
        pass 

    @abstractmethod
    def accept(self, visitor: Visitor):
        pass

class Literal(Expr):
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
    
class Unary(Expr): 
    def __init__(self, op, expr: Expr):
        self.op = op
        self.expr = expr
    
    def __str__(self):
        return f"({self.op.lex} {self.expr})"
    
    def accept(self, visitor):
        return visitor.visitUnaryExpr(self)

class Grouping(Expr): 
    def __init__(self, expr: Expr):
        self.expr = expr
    
    def __str__(self):
        return f"(group {self.expr})"
    
    def accept(self, visitor):
        return visitor.visitGroupingExpr(self)

class Binary(Expr): 
    def __init__(self, op, left = None, right = None):
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.op.lex} {self.left} {self.right})"
    
    def accept(self, visitor):
        return visitor.visitBinaryExpr(self)