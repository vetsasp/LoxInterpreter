import sys


def main():
    # print("Logs from your program will appear here!", file=sys.stderr)

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
    
    ex, ln = 0, 1

    tok = []

    for c in file_contents:
        if c == "\n":
            ln += 1
        elif c == "(":
            tok.append("LEFT_PAREN ( null")
        elif c == ")":
            tok.append("RIGHT_PAREN ) null")
        elif c == "{":
            tok.append("LEFT_BRACE { null")
        elif c == "}":
            tok.append("RIGHT_BRACE } null")
        elif c == ",":
            tok.append("COMMA , null")
        elif c == ".":
            tok.append("DOT . null")
        elif c == "-":
            tok.append("MINUS - null")
        elif c == "+":
            tok.append("PLUS + null")
        elif c == ";":
            tok.append("SEMICOLON ; null")
        elif c == "*":
            tok.append("STAR * null")
        elif c == "!":
            tok.append("BANG ! null")
        elif c == "=":
            if len(tok) > 0 and tok[-1] == "EQUAL = null":
                tok.pop()
                tok.append("EQUAL_EQUAL == null")
            elif len(tok) > 0 and tok[-1] == "BANG ! null":
                tok.pop()
                tok.append("BANG_EQUAL != null")
            else:
                tok.append("EQUAL = null")
        else:
            print(f"[line {ln}] Error: Unexpected character: {c}", file=sys.stderr)
            ex = 65
            tok.append("")


    for t in tok:
        if t != "":
            print(t)
    
    print("EOF  null")

    exit(ex)

if __name__ == "__main__":
    main()
