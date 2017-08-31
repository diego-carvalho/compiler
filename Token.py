class Token:
	def __init__(self, name, lexical, line):
		self.name = name
		self.lexical = lexical
		self.line = [line]

	def __str__(self):
		return "token [name: " + self.name + ", lexical: " + self.lexical + " , line: " + str(self.line) + "]"

	def __repr__(self):
		return "token [name: " + self.name + ", lexical: " + self.lexical + " , line: " + str(self.line) + "]" + "\n"

	def setLine(self, line):
		self.line.append(line)