from app.tokens import Token
from app.tokens import TokenType

from app.expressions import Visitor
from app.expressions import Expr


class MyRuntimeError(Exception): 
    def __init__(self, token: Token, msg: str):
        super(msg)
        self.token = token 


class Evaluator(Visitor):
    def visit_literal_expr(self, expr): 
        return expr.val 

    def visit_unary_expr(self, expr): 
        child = _evaluate(expr.expr)

        if expr.op.type == TokenType.BANG:
            return not isTruthful(child)
        elif expr.op.type == TokenType.MINUS:
            checkNumberOperands(expr.op, child)
            return -child
        
        print("unary evaluate failed")

    def visit_grouping_expr(self, expr): 
        return _evaluate(expr.expr)

    def visit_binary_expr(self, expr): 
        left = _evaluate(expr.left)
        right = _evaluate(expr.right)

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
            return left / right 
        elif t == TokenType.STAR:
            checkNumberOperands(expr.op, left, right)
            return left * right 
        
        print("binary evaluate failed")

# evaluation helpers
def evaluate(expr: Expr):
    # This evaluation is functionally correct
    # however, aesthetic differences from the book must be addressed
    res = _evaluate(expr)

    # aesthetic changes 
    if isinstance(res, float) and res.is_integer():
        return int(res)
    if isinstance(res, bool):
        return "true" if res else "false"
    return res

def _evaluate(expr: Expr): 
    return expr.accept(Evaluator())

def isTruthful(obj) -> bool:
    if obj == "nil":
        return False
    if isinstance(obj, bool):
        return obj
    return True

def checkNumberOperands(operator: Token, *operands):
    for operand in operands:
        if not isinstance(operand, float):
            raise MyRuntimeError(operator, "Operands must be numbers.")
    return 
