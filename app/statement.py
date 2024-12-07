from abc import ABC, abstractmethod

from app.tokens import Token


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

        @abstractmethod 
        def visitVarStmt(self, stmt):
            pass 

        '''
        @abstractmethod 
        def visitBlockStmt(self, stmt):
            pass
        
        @abstractmethod 
        def visitClassStmt(self, stmt):
            pass
        
        @abstractmethod 
        def visitFunctionStmt(self, stmt):
            pass
        
        @abstractmethod 
        def visitIfStmt(self, stmt):
            pass
        
        @abstractmethod 
        def visitReturnStmt(self, stmt):
            pass
        
        @abstractmethod 
        def visitWhileStmt(self, stmt):
            pass
        
        '''


class StmtExpression(Stmt):
    def __init__(self, expr): 
        self.expression = expr

    def accept(self, visitor):
        return visitor.visitExpressionStmt(self)

class StmtPrint(Stmt):
    def __init__(self, expr):
        self.expression = expr

    def accept(self, visitor):
        return visitor.visitPrintStmt(self)
    
class StmtVariable(Stmt):
    def __init__(self, name: Token, initializer):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor):
        return visitor.visitVarStmt(self)
    
class StmtBlock(Stmt):
    def __init__(self, statements: list[Stmt]):
        self.statements = statements

    def accept(self, visitor):
        return visitor.visitBlockStmt(self)
    

'''
    STATUS: 
        Reached 8.2 in the book
        - Global Variables
        Error handling suspended
        Test cases cannot be past until reimplemented
        Following book more strictly now. 

        legacy code will be removed after next successful submit. 
'''