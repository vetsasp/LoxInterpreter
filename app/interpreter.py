from app.tokens import TokenType
from app.tokens import Token
from app.tokenizer import Tokenizer
from app.parser import Parser

import sys

class Interpreter:
    def __init__(self, text: str = ""):
        self._text = text
        self._tokenizer = Tokenizer(text)
        self.hadError = False

    def run(self, cmd: str):
        tokens, ex = self._tokenizer.tokenize() 

        if cmd == "tokenize":
            self._tokenizer.printTokens()
            return ex

        if ex != 0:
            # print("Tokenizing Failed. Cannot Parse. Exit Code", ex)
            return ex

        self._parser = Parser(self, tokens)
        self._parser.parse()

        if cmd == "parse" and not self.hadError:
            self._parser.printTree()
        
        if self.hadError:
            exit(65)
        
    def error(self, token: Token, msg: str):
        if (token.token_type == TokenType.EOF):
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