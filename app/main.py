from app.lox import Lox

import sys


def main():
    # print("Logs here", file=sys.stderr)

    argc = len(sys.argv)

    if argc < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    lox = Lox()



    if argc == 1:
        lox.runPrompt() 
    else:
        cmd = sys.argv[1]
        validCommands = ["tokenize", "parse", "evaluate", "run"]

        if cmd not in validCommands:
            print(f"Unknown command: {cmd}", file=sys.stderr)
            exit(1)
        lox.runFile(sys.argv[2], cmd)



if __name__ == "__main__":
    main()