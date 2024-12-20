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
        def visitCallExpr(self, expr):
            pass

        @abstractmethod
        def visitLogicalExpr(self, expr):
            pass

        @abstractmethod
        def visitGetExpr(self, expr):
            pass

        @abstractmethod
        def visitSetExpr(self, expr):
            pass

        @abstractmethod
        def visitThisExpr(self, expr):
            pass

        @abstractmethod
        def visitSuperExpr(self, expr):
            pass

    # @abstractmethod
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

    # def __str__(self):
    #     return f"{self.name.lex}"   # TODO 
    
    def accept(self, visitor):
        return visitor.visitVariableExpr(self)
    
class ExprAssign(Expr):
    def __init__(self, name: Token, val: Expr):
        self.name = name
        self.val = val

    # def __str__(self):
    #     return f"{self.name.lex} = {self.val}"
        
    def accept(self, visitor):
        return visitor.visitAssignExpr(self)
    
class ExprLogical(Expr):
    def __init__(self, left: Expr, op: Token, right: Expr):
        self.left = left
        self.op = op
        self.right = right
    
    def accept(self, visitor):
        return visitor.visitLogicalExpr(self)
    
class ExprCall(Expr):
    def __init__(self, callee: Expr, paren: Token, args: list[Expr]):
        self.callee = callee
        self.paren = paren
        self.args = args 

    def accept(self, visitor):
        return visitor.visitCallExpr(self)
    

# Class Expressions 

class ExprGet(Expr):
    def __init__(self, obj: Expr, name: Token):
        self.obj = obj
        self.name = name

    def accept(self, visitor):
        return visitor.visitGetExpr(self)
    
class ExprSet(Expr):
    def __init__(self, obj: Expr, name: Token, val: Expr):
        self.obj = obj
        self.name = name
        self.val = val

    def accept(self, visitor):
        return visitor.visitSetExpr(self)

class ExprThis(Expr):
    def __init__(self, keyword: Token):
        self.keyword = keyword

    def accept(self, visitor):
        return visitor.visitThisExpr(self)
    
class ExprSuper(Expr):
    def __init__(self, keyword: Token, method: Token):
        self.keyword = keyword
        self.method = method

    def accept(self, visitor):
        return visitor.visitSuperExpr(self)