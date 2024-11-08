import sys
import re
from enum import Enum


class Tokenizer:
    def __init__(self, text):
        self._text = text
        self._pos = 0
        self._line = 1
        self._tokens = []

    def __len__(self) -> int:
        return len(self._text)
    
    def top(self) -> str:
        if self._pos >= len(self._text):
            return None
        else:
            return self._text[self._pos]
        
    def nxt(self) -> None:
        if self._pos >= len(self._text):
            return None
        else:
            if self.top() == "\n":
                self._line += 1
            self._pos += 1
    
    def tok(self, t: str) -> None:
        self._tokens.append(t)

    def pop(self) -> str:
        return self._tokens.pop()
    
    def tokens(self) -> list:
        return self._tokens
    
    def line(self) -> int:
        return self._line
    
    def inc_line(self) -> None:
        while (c := self.top()) != "\n" and c != None:
            # print("skipping", c)
            self.nxt()

    def isPrev(self, s: str) -> bool:
        return self._pos > 0 and self._tokens[-1].startswith(s)
    
    def parseString(self) -> bool:
        match = re.match(r'"[^"]*"', self._text[self._pos:], re.DOTALL)
        if not match:
            self._pos = len(self._text)
            return False
        s = match.group()

        self._pos += len(s) - 1

        self.tok(f"STRING {s} {s[1:-1]}")

        return True

    def parseNum(self) -> bool:
        match = re.match(r'\d+', self._text[self._pos:])

        if match:
            n = match.group()
            self._pos += len(n) - 1
            self.tok(f"NUMBER {n} {float(n)}")
            return True
        else:
            print("can this even happen??")
            return False
    
    def parseIdent(self) -> bool:
        match = re.match(r'[a-zA-Z_][a-zA-Z0-9_]*', self._text[self._pos:])
        if match: 
            keyword = match.group()
            self._pos += len(keyword) - 1
            if not self.checkReserved(keyword):
                self.tok(f"IDENTIFIER {keyword} null")
            return True
        print("Parse Identifier Failed", file=sys.stderr)
        return False 

    def checkReserved(self, kw: str) -> bool: 
        keywords = {
            "and", "class", "else", "false", "for", "fun", "if", "nil", "or", "print", "return", "super", "this", "true", "var", "while"
        }
        if kw in keywords:
            self.tok(f"{kw.upper()} {kw} null")
            return True
        return False

    def tokenize(self) -> int:
        ex = 0
        while c := self.top():
            # print("Token: " + c) # debug
            if c == " " or c == "\t" or c == "\n":
                pass
            elif c == "(":
                self.tok("LEFT_PAREN ( null")
            elif c == ")":
                self.tok("RIGHT_PAREN ) null")
            elif c == "{":
                self.tok("LEFT_BRACE { null")
            elif c == "}":
                self.tok("RIGHT_BRACE } null")
            elif c == ",":
                self.tok("COMMA , null")
            elif c == ".":
                # Check if Decimal
                if self.isPrev("NUMBER"):
                    self.nxt()
                    if self.parseNum():
                        decimal = self.pop().split()[1]
                        whole = self.pop().split()[1]
                        if float(decimal) == 0:
                            self.tok(f"NUMBER {whole}.{decimal} {whole}.0")
                        else:
                            self.tok(f"NUMBER {whole}.{decimal} {whole}.{decimal}")
                    else:
                        self.tok("DOT . null")
                else:
                    self.tok("DOT . null")
            elif c == "-":
                self.tok("MINUS - null")
            elif c == "+":
                self.tok("PLUS + null")
            elif c == ";":
                self.tok("SEMICOLON ; null")
            elif c == "*":
                self.tok("STAR * null")
            elif c == "!":
                self.tok("BANG ! null")
            elif c == "<":
                self.tok("LESS < null")
            elif c == ">":
                self.tok("GREATER > null")
            elif c == "=":
                if self.isPrev("EQUAL ="):
                    self.pop()
                    self.tok("EQUAL_EQUAL == null")
                elif self.isPrev("BANG !"):
                    self.pop()
                    self.tok("BANG_EQUAL != null")
                elif self.isPrev("LESS <"):
                    self.pop()
                    self.tok("LESS_EQUAL <= null")
                elif self.isPrev("GREATER >"):
                    self.pop()
                    self.tok("GREATER_EQUAL >= null")
                else:
                    self.tok("EQUAL = null")
            elif c == "/":
                if self.isPrev("SLASH /"):
                    # Comment 
                    self.pop()
                    self.inc_line()
                else:
                    self.tok("SLASH / null")
            elif c == "\"":
                # String
                if not self.parseString():
                    print(f"[line {self.line()}] Error: Unterminated string.", file=sys.stderr)
                    ex = 65
            elif c in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
                # Number
                self.parseNum()
            elif c.isalpha() or c == "_":
                # Identifier
                self.parseIdent()
            else:
                print(f"[line {self.line()}] Error: Unexpected character: {c}", file=sys.stderr)
                ex = 65
                self.tok("")
            
            self.nxt()
        
        self.tok("EOF  null")

        return ex

class Parser:
    class Expression(Enum):
        LITERAL = 0
        UNARY = 1
        BINARY = 2
        GROUPING = 3

    class ST:
        def __init__(self, t, val, left = None, right = None):
            self.type = t
            self.val = val
            self.left, self.right = left, right 

    def __init__(self, tokens):
        self._tokens = tokens
        self.head = None 

    def typeMap(self, token: str) -> Expression:
        typeMap = {
            "NUMBER": Parser.Expression.LITERAL, 
            "STRING": Parser.Expression.LITERAL, 
            "TRUE": Parser.Expression.LITERAL, 
            "FALSE": Parser.Expression.LITERAL, 
            "NIL": Parser.Expression.LITERAL,
            "EOF": None
        }

        return typeMap[token]

    def parse(self) -> bool:
        for token in self._tokens:
            # print(token)
            split = token.split()
            expType = self.typeMap(split[0])

            if expType == Parser.Expression.LITERAL:
                self.head = Parser.ST(expType, split[1])
    
    def printTree(self) -> None: 
        self._printTree(self.head)

    def _printTree(self, node: ST) -> None:
        if node:
            print(node.val)
            self._printTree(node.left)
            self._printTree(node.right)


def main():
    # print("Logs here", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize" and command != "parse":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()
    
    tknzr = Tokenizer(file_contents)

    ex = tknzr.tokenize()

    tokens = tknzr.tokens()

    if command == "tokenize":
        for token in tokens:
            if token != "":
                print(token)
        exit(ex)

    if ex != 0:
        print("Tokenizing Failed. Cannot Parse. Exit Code", ex)
        exit(ex)

    psr = Parser(tokens)

    psr.parse()

    psr.printTree()

if __name__ == "__main__":
    main()


