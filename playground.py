s = """This
is a string
of some length 
and I'm going to write
some more text

and some more
and its multiline wooo
"""

# print(s)

class Reader:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self._line = 1
    
    def read(self):
        if self.pos >= len(self.text):
            return None
        else:
            c = self.text[self.pos]
            self.pos += 1
            if c == "\n":
                self._line += 1
            return c
    
    def line(self):
        return self._line
    
    def skip_line(self):
        while self.read() != "\n":
            pass

r = Reader(s)
print(r.read())
print(r.line())
r.skip_line()
print(r.read())


print(r.line())