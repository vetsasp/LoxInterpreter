import sys

from app.tokens import Token, TokenType
from app.tokenize import Tokenizer
from app.parser import Parser
from app.runtime import MyRuntimeError
from app.interpreter import Interpreter
from app.statement import Stmt


class Lox:
    def __init__(self):
        self.hadError = False
        self.hadRuntimeError = False
        self.cmd = ""
        self.ignore_error = False

    def runPrompt(self):
        inp = ""

        while inp != "exit":
            line = input("> ")
            if inp != "exit":
                if line == "" or line == "\n":
                    continue 
                self.run(line)
                self.hadError = False

    def runFile(self, path: str, cmd: str = ""):
        with open(path) as file:
            file_contents = file.read()
        self.run(file_contents, cmd)

        if self.hadError:
            exit(65)
        if self.hadRuntimeError:
            exit(70)

    def run(self, line: str, cmd: str = ""):
        t = Tokenizer(self, line)
        tokens: list[Token] = t.tokenize()

        if cmd == "tokenize":
            t.printTokens()
            return
        
        if self.hadError:
            return

        ignore_error_case = {"parse", "evaluate"}
        # ignore_error_case = {"evaluate"}
        if cmd in ignore_error_case:
            self.ignore_error = True
        
        p = Parser(self, tokens)
        i = Interpreter(self)

        statements: list[Stmt] = p.parse()

        if cmd == "parse":
            if self.hadError:
                return
            for s in statements:
                print(s.expression)
            return
        
        if cmd == "evaluate":
            try:
                i.evaluate_LEGACY(statements[0])
            except MyRuntimeError as e:
                self.report(e.token.line, "", e.msg)
            return


        if self.hadError:
            return
        

        # print("Interpreting...")    # DEBUG
        i.interpret(statements)


    '''
    LEGACY CODE
        expression = p.parse()
        
        if self.hadError:
            return

        if cmd == "parse":
            print(expression)
            return
        
        i = Interpreter(self)

        if cmd == "evaluate":
            try:
                i.interpret(expression)
            except MyRuntimeError as e:
                self.report(e.token.line, "", e.msg)
    '''
    
        


    def report(self, line: int, where: str, msg: str):
        print(f"[line {line}] Error{where}: {msg}", file=sys.stderr)
        self.hadError = True

    def tokenError(self, line: int, msg: str):
        self.report(line, "", msg)

    def parseError(self, token: Token, msg: str):
        if (token.type == TokenType.EOF):
            self.report(token.line, " at end", msg)
        else:
            self.report(token.line, f" at '{token.lex}'", msg)

    def runtimeError(self, err: MyRuntimeError):
        print(f"{err.msg}\n[line {err.token.line}]", file=sys.stderr)
        self.hadRuntimeError = True