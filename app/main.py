from app.interpreter import Interpreter

import sys


def main():
    # print("Logs here", file=sys.stderr)

    if len(sys.argv) < 3:
        print("Usage: ./your_program.sh tokenize <filename>", file=sys.stderr)
        exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    validCommands = ["tokenize", "parse", "evaluate"]

    if command not in validCommands:
        print(f"Unknown command: {command}", file=sys.stderr)
        exit(1)

    with open(filename) as file:
        file_contents = file.read()
    
    lox = Interpreter(file_contents)

    lox.run(command)


if __name__ == "__main__":
    main()


