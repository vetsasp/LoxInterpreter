from app.tokens import TokenType
from app.tokens import Token
from app.tokenizer import Tokenizer
from app.parser import Parser

import sys


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
    
    tsr = Tokenizer(file_contents)

    tokens, ex = tsr.tokenize()

    if command == "tokenize":
        tsr.printTokens()
        exit(ex)
    
    if ex != 0:
        print("Tokenizing Failed. Cannot Parse. Exit Code", ex)
        exit(ex)

    psr = Parser(tokens)

    psr.parse()

    psr.printTree()


if __name__ == "__main__":
    main()


