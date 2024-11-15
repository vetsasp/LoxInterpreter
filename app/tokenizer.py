from app.tokens import TokenType
from app.tokens import Token

import re
import sys


class Tokenizer:
    def __init__(self, text):
        self._text = text
        self._pos = 0
        self._line = 1
        self._tokens = []
        self._d = {
            "(": TokenType.LEFT_PAREN, 
            ")": TokenType.RIGHT_PAREN,
            "{": TokenType.LEFT_BRACE,
            "}": TokenType.RIGHT_BRACE,
            ",": TokenType.COMMA,
            "-": TokenType.MINUS,
            "+": TokenType.PLUS,
            ";": TokenType.SEMICOLON,
            "*": TokenType.STAR,
            "!": TokenType.BANG,
            ">": TokenType.GREATER,
            "<": TokenType.LESS,
        }

    def __len__(self) -> int:
        return len(self._text)
    
    def top(self) -> str:
        if self._pos >= len(self._text):
            return None
        else:
            return self._text[self._pos]
        
    def advance(self) -> None:
        if self._pos >= len(self._text):
            return None
        else:
            if self.top() == "\n":
                self._line += 1
            self._pos += 1
    
    def tok(self, t: TokenType, lex, lit = "null") -> None:
        self._tokens.append(Token(t, lex, lit))

    def pop(self) -> Token:
        return self._tokens.pop()
    
    def tokens(self) -> list[Token]:
        return self._tokens
    
    def line(self) -> int:
        return self._line
    
    def printTokens(self):
        for token in self._tokens:
            if token.token_type != None:
                print(token)

    def inc_line(self) -> None:
        while (c := self.top()) != "\n" and c != None:
            # print("skipping", c)
            self.advance()

    def isPrev(self, s: TokenType) -> bool:
        return self._pos > 0 and self._tokens[-1].token_type == s
    
    def parseString(self) -> bool:
        match = re.match(r'"[^"]*"', self._text[self._pos:], re.DOTALL)
        if not match:
            self._pos = len(self._text)
            return False
        s = match.group()

        self._pos += len(s) - 1

        self.tok(TokenType.STRING, s, s[1:-1])

        return True

    def parseNum(self) -> bool:
        match = re.match(r'\d+', self._text[self._pos:])

        if match:
            n = match.group()
            self._pos += len(n) - 1
            self.tok(TokenType.NUMBER, n, float(n))
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
                self.tok(TokenType.IDENTIFIER, keyword)
            return True
        print("Parse Identifier Failed", file=sys.stderr)
        return False 

    def checkReserved(self, kw: str) -> bool: 
        keywords = {
            "and": TokenType.AND,
            "class": TokenType.CLASS,
            "else": TokenType.ELSE,
            "false": TokenType.FALSE,
            "for": TokenType.FOR,
            "fun": TokenType.FUN,
            "if": TokenType.IF,
            "nil": TokenType.NIL,
            "or": TokenType.OR,
            "print": TokenType.PRINT,
            "return": TokenType.RETURN,
            "super": TokenType.SUPER,
            "this": TokenType.THIS,
            "true": TokenType.TRUE,
            "var": TokenType.VAR,
            "while": TokenType.WHILE
        }
        if kw in keywords:
            self.tok(keywords[kw], kw)
            return True
        return False

    def tokenize(self) -> tuple[list[Token], int]:
        ex = 0
        while c := self.top():
            # print("Token: " + c) # debug
            if c == " " or c == "\t" or c == "\n":
                pass
            elif c in self._d:
                self.tok(self._d[c], c)
            elif c == ".":
                # Check if Decimal
                if self.isPrev(TokenType.NUMBER):
                    self.advance()
                    if self.parseNum():
                        decimal = self.pop().lex
                        whole = self.pop().lex
                        n = f"{whole}.{decimal}"
                        self.tok(TokenType.NUMBER, n, float(n))
                    else:
                        self.tok(TokenType.DOT, ".")
                else:
                    self.tok(TokenType.DOT, ".")
            # elif c == "-":
            #     self.tok(TokenType.MINUS, "-")
            # elif c == "+":
            #     self.tok(TokenType.PLUS, "+")
            # elif c == ";":
            #     self.tok(TokenType.SEMICOLON, ";")
            # elif c == "*":
            #     self.tok(TokenType.STAR, "*")
            # elif c == "!":
            #     self.tok(TokenType.BANG, "!")
            # elif c == "<":
            #     self.tok(TokenType.LESS, "<")
            # elif c == ">":
            #     self.tok(TokenType.GREATER, ">")
            elif c == "=":
                if self.isPrev(TokenType.EQUAL):
                    self.pop()
                    self.tok(TokenType.EQUAL_EQUAL, "==")
                elif self.isPrev(TokenType.BANG):
                    self.pop()
                    self.tok(TokenType.BANG_EQUAL, "!=")
                elif self.isPrev(TokenType.LESS):
                    self.pop()
                    self.tok(TokenType.LESS_EQUAL, "<=")
                elif self.isPrev(TokenType.GREATER):
                    self.pop()
                    self.tok(TokenType.GREATER_EQUAL, ">=")
                else:
                    self.tok(TokenType.EQUAL, "=")
            elif c == "/":
                if self.isPrev(TokenType.SLASH):
                    # Comment 
                    self.pop()
                    self.inc_line()
                else:
                    self.tok(TokenType.SLASH, "/")
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
                self.tok(None, None)
            
            self.advance()
        
        self.tok(TokenType.EOF, "", "null")

        return self._tokens, ex
    
    def _reset(self, text: str) -> None:
        self._pos = 0
        self._line = 1
        self._tokens = []
        self._text = text


if __name__ == "__main__":
    # Full test suite

    text = "({*+;+-})"
    print(text)
    t = Tokenizer(text)
    tokens, ex = t.tokenize()
    t.printTokens()

    text = "1 + 2.5"
    print(text)
    t._reset(text)
    tokens, ex = t.tokenize()
    t.printTokens()

    text = "\"hello world\""
    print(text)
    t._reset(text)
    tokens, ex = t.tokenize()
    t.printTokens()

