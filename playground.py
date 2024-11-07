import re 


s = "a"

match = re.match(r'[a-zA-Z_][a-zA-Z0-9_]*', s)

print(match)