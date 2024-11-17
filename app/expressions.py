from app.tokens import Token
from app.tokens import TokenType

from abc import ABC, abstractmethod


class Visitor(ABC):
    @abstractmethod
    def visit_literal_expr(self, expr): 
        pass

    @abstractmethod
    def visit_unary_expr(self, expr): 
        pass

    @abstractmethod
    def visit_grouping_expr(self, expr): 
        pass

    @abstractmethod
    def visit_binary_expr(self, expr): 
        pass


class Expr(ABC):
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
        return str(self.val)
    
    def accept(self, visitor):
        return visitor.visit_literal_expr(self)
    
class Unary(Expr): 
    def __init__(self, op, expr: Expr):
        self.op = op
        self.expr = expr
    
    def __str__(self):
        return f"({self.op.lex} {self.expr})"
    
    def accept(self, visitor):
        return visitor.visit_unary_expr(self)

class Grouping(Expr): 
    def __init__(self, expr: Expr):
        self.expr = expr
    
    def __str__(self):
        return f"(group {self.expr})"
    
    def accept(self, visitor):
        return visitor.visit_grouping_expr(self)

class Binary(Expr): 
    def __init__(self, op, left = None, right = None):
        self.op = op
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.op.lex} {self.left} {self.right})"
    
    def accept(self, visitor):
        return visitor.visit_binary_expr(self)
    

# defining Visitors 

# Evaluation
class Evaluator(Visitor):
    def visit_literal_expr(self, expr): 
        return expr.val 

    def visit_unary_expr(self, expr): 
        child = evaluate(expr.expr)

        if expr.op.type == TokenType.BANG:
            return not isTruthful(child)
        elif expr.op.type == TokenType.MINUS:
            checkNumberOperands(expr.op, child)
            return -child
        
        print("unary evaluate failed")

    def visit_grouping_expr(self, expr): 
        return evaluate(expr.expr)

    def visit_binary_expr(self, expr): 
        left = evaluate(expr.left)
        right = evaluate(expr.right)

        t = expr.op.type 

        if t == TokenType.GREATER:
            checkNumberOperands(expr.op, left, right)
            return left > right 
        elif t == TokenType.GREATER_EQUAL:
            checkNumberOperands(expr.op, left, right)
            return left >= right 
        elif t == TokenType.LESS:
            checkNumberOperands(expr.op, left, right)
            return left < right 
        elif t == TokenType.LESS_EQUAL:
            checkNumberOperands(expr.op, left, right)
            return left <= right 
        elif t == TokenType.BANG_EQUAL:
            return not left == right 
        elif t == TokenType.EQUAL:
            return left == right 
        elif t == TokenType.MINUS:
            checkNumberOperands(expr.op, left, right)
            return left - right
        elif t == TokenType.PLUS:
            return left + right 
        elif t == TokenType.SLASH:
            checkNumberOperands(expr.op, left, right)
            return left // right 
        elif t == TokenType.STAR:
            checkNumberOperands(expr.op, left, right)
            return left * right 
        
        print("binary evaluate failed")

# evaluation helpers
class MyRuntimeError(Exception): 
    def __init__(self, token: Token, msg: str):
        super(msg)
        self.token = token 

def evaluate(expr: Expr): 
    return expr.accept(Evaluator())

def isTruthful(obj) -> bool:
    if obj == None:
        return False
    if isinstance(obj, bool):
        return obj
    return True

def checkNumberOperands(operator: Token, *operands):
    for operand in operands:
        if not isinstance(operand, float):
            raise MyRuntimeError(operator, "Operands must be numbers.")
    return 

if __name__ == "__main__":
    pass