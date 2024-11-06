import sys


class Tokenizer:
    def __init__(self, text):
        self._text = text
        self._pos = 0
        self._line = 1
        self._tokens = []
    
    def top(self) -> str:
        if self._pos >= len(self._text):
            return None
        else:
            return self._text[self._pos]
            self._pos += 1
            if c == "\n":
                self._line += 1
            return c
        
    def nxt(self) -> None:
        if self._pos >= len(self._text):
            return None
        else:
            self._pos += 1
            if self.top() == "\n":
                self._line += 1
    
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
        return self._pos > 0 and self._tokens[-1] == s






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
        if c == "\n":
            continue
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
            if t.isPrev("EQUAL = null"):
                t.pop()
                t.tok("EQUAL_EQUAL == null")
            elif t.isPrev("BANG ! null"):
                t.pop()
                t.tok("BANG_EQUAL != null")
            elif t.isPrev("LESS < null"):
                t.pop()
                t.tok("LESS_EQUAL <= null")
            elif t.isPrev("GREATER > null"):
                t.pop()
                t.tok("GREATER_EQUAL >= null")
            else:
                t.tok("EQUAL = null")
        elif c == "/":
            if t.isPrev("SLASH / null"):
                # Comment 
                t.pop()
                t.inc_line()
            else:
                t.tok("SLASH / null")
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


