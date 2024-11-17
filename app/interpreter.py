from app.tokens import TokenType
from app.tokens import Token
from app.tokenizer import Tokenizer
from app.parser import Parser
from app.expressions import Expr
from app.evaluate import evaluate
from app.evaluate import MyRuntimeError

import sys

class Interpreter:
    def __init__(self, text: str = ""):
        self._text = text
        self.hadError = False

    def errorCheck(self):
        if self.hadError:
            exit(65)

    def run(self, cmd: str):
        tokenizer = Tokenizer(self._text)
        tokens = tokenizer.tokenize() 

        if cmd == "tokenize":
            tokenizer.printTokens()
            if tokenizer.hadError():
                exit(65)
            return

        if tokenizer.hadError():
            exit(65)

        # tokenizer.printTokens() # debug: print tokens 

        parser = Parser(self, tokens)
        expression = parser.parse()

        self.errorCheck()

        if cmd == "parse":
            print(expression)

        # print(expression) # debug
        
        if self.hadError:
            exit(65)

        if cmd == "evaluate":
            self.interpret(expression)

    def interpret(self, expression: Expr): 
        try: 
            value = evaluate(expression)
            print(value)
        except MyRuntimeError as e:
            print(e, file=sys.stderr)
            exit(70)
        
        
    def error(self, token: Token, msg: str):
        if (token.type == TokenType.EOF):
            self.report(token.line, " at end", msg)
        else:
            self.report(token.line, f"at '{token.lex}'", msg)

    def report(self, line: int, where: str, msg: str):
        print(f"[line {line}] Error {where}: {msg}", file=sys.stderr)
        self.hadError = True


if __name__ == "__main__":
    pass
    # print("scan: ", keyword.iskeyword("scan"))
    # print("run: ", keyword.iskeyword("run"))