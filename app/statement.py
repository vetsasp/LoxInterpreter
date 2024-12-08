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

        @abstractmethod 
        def visitIfStmt(self, stmt):
            pass

        @abstractmethod 
        def visitWhileStmt(self, stmt):
            pass
        
        @abstractmethod 
        def visitBlockStmt(self, stmt):
            pass
        
        @abstractmethod 
        def visitFunctionStmt(self, stmt):
            pass

        @abstractmethod 
        def visitReturnStmt(self, stmt):
            pass

        '''
        @abstractmethod 
        def visitClassStmt(self, stmt):
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

class StmtIf(Stmt):
    def __init__(self, condition, thenBranch: Stmt, elseBranch: Stmt):
        self.condition = condition
        self.thenBranch = thenBranch
        self.elseBranch = elseBranch

    def accept(self, visitor):
        return visitor.visitIfStmt(self)

class StmtWhile(Stmt):
    def __init__(self, condition, body: Stmt):
        self.condition = condition
        self.body = body

    def accept(self, visitor):
        return visitor.visitWhileStmt(self)
    
class StmtFunction(Stmt):
    def __init__(self, name: Token, params: list[Token], body: list[Stmt]):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor):
        return visitor.visitFunctionStmt(self)

class StmtReturn(Stmt):
    def __init__(self, keyword: Token, value):
        self.keyword = keyword
        self.value = value

    def accept(self, visitor):
        return visitor.visitReturnStmt(self)