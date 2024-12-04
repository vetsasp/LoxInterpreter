from abc import ABC, abstractmethod


class Stmt(ABC):
    '''
    Expression  : Expr expression
    Print       : Expr expression
    '''
    @abstractmethod
    def accept(self, visitor): 
        pass

    class Visitor(ABC):
        @abstractmethod 
        def visitExpressionStmt(self, expr):
            pass 

        @abstractmethod 
        def visitPrintStmt(self, stmt):
            pass 

    class Expression(Stmt):
        def __init__(self, expr): 
            self.expression = expr

        def accept(self, visitor):
            return visitor.visitExpressionStmt(self)

    class Print(Stmt):
        def __init__(self, expr):
            self.expression = expr

        def accept(visitor):
            pass 