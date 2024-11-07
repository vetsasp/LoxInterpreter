import sys
import re


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
        # match = re.match(r'\d+\.?\d*', self._text[self._pos:])
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
        match = re.match(r'[a-zA-Z_][a-zA-Z0-9_]+', self._text[self._pos:])
        if match: 
            ident = match.group()
            self._pos += len(ident) - 1
            self.tok(f"IDENTIFIER {ident} null")
            return True
        return False 






def main():
    # print("Logs here", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command != "tokenize":
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()
    
    t = Tokenizer(file_contents)

    ex = 0


    while c := t.top():
        # print("Token: " + c) # debug
        if c == " " or c == "\t" or c == "\n":
            pass
        elif c == "(":
            t.tok("LEFT_PAREN ( null")
        elif c == ")":
            t.tok("RIGHT_PAREN ) null")
        elif c == "{":
            t.tok("LEFT_BRACE { null")
        elif c == "}":
            t.tok("RIGHT_BRACE } null")
        elif c == ",":
            t.tok("COMMA , null")
        elif c == ".":
            # Check if Decimal
            if t.isPrev("NUMBER"):
                t.nxt()
                if t.parseNum():
                    decimal = t.pop().split()[1]
                    whole = t.pop().split()[1]
                    if float(decimal) == 0:
                        t.tok(f"NUMBER {whole}.{decimal} {whole}.0")
                    else:
                        t.tok(f"NUMBER {whole}.{decimal} {whole}.{decimal}")
                else:
                    t.tok("DOT . null")
            else:
                t.tok("DOT . null")
        elif c == "-":
            t.tok("MINUS - null")
        elif c == "+":
            t.tok("PLUS + null")
        elif c == ";":
            t.tok("SEMICOLON ; null")
        elif c == "*":
            t.tok("STAR * null")
        elif c == "!":
            t.tok("BANG ! null")
        elif c == "<":
            t.tok("LESS < null")
        elif c == ">":
            t.tok("GREATER > null")
        elif c == "=":
            if t.isPrev("EQUAL ="):
                t.pop()
                t.tok("EQUAL_EQUAL == null")
            elif t.isPrev("BANG !"):
                t.pop()
                t.tok("BANG_EQUAL != null")
            elif t.isPrev("LESS <"):
                t.pop()
                t.tok("LESS_EQUAL <= null")
            elif t.isPrev("GREATER >"):
                t.pop()
                t.tok("GREATER_EQUAL >= null")
            else:
                t.tok("EQUAL = null")
        elif c == "/":
            if t.isPrev("SLASH /"):
                # Comment 
                t.pop()
                t.inc_line()
            else:
                t.tok("SLASH / null")
        elif c == "\"":
            # String
            if not t.parseString():
                print(f"[line {t.line()}] Error: Unterminated string.", file=sys.stderr)
                ex = 65
        elif c in {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}:
            # Number
            t.parseNum()
        elif c.isalpha() or c == "_":
            # Identifier
            t.parseIdent()
        else:
            print(f"[line {t.line()}] Error: Unexpected character: {c}", file=sys.stderr)
            ex = 65
            t.tok("")
        
        t.nxt()

        # print(t.tokens()) # debug


    for t in t.tokens():
        if t != "":
            print(t)
    
    print("EOF  null")

    exit(ex)

if __name__ == "__main__":
    main()


