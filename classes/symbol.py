class Symbol:
    def __init__(self, lexical, type, line, value):
        self.lexical = lexical
        self.type = type
        self.line = line
        self.value = value

    def __str__(self):
        return "Symbol [lexical: " + self.lexical + " , line: " + str(self.line) + " , type: " + self.type + " , value: " + self.value + "]"

    def __repr__(self):
        return "Symbol [lexical: " + self.lexical + " , line: " + str(self.line) + " , type: " + self.type + " , value: " + self.value + "]" + "\n"
