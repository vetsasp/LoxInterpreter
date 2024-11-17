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
    


if __name__ == "__main__":
    print(68 / 5)
    print(68 // 5)