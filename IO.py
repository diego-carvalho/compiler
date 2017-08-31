import sys


from collections import deque


class Char():
	def __init__(self, char, line):
		self.char = char
		self.line = line

	def __str__(self):
		return "char [ char: " + self.char + ", line: " + str(self.line)

	def __repr__(self):
		return "" + self.char


class IO:
	def __init__(self, filepath):
		try:
			self.file = open(filepath, 'r')
			self.buffer = deque('', 10)
			self.line = []
			self.lineNumber = 0
			
			
		except:
			print("Erro ao abrir o arquivo tente novamente, " + filepath)
			sys.exit(1)

		self.getInitialDqeue()

	def getInitialDqeue(self):
		for i in range(10):
			c = self.getChar()
			self.buffer.append(c)

	def getNextChar(self):
		char = self.buffer.popleft()
		if char.char != False:
			c = self.getChar()
			self.buffer.append(c)
		return char

	def getChar(self):
		if len(self.line) == 0:
			line = self.file.readline()
			self.lineNumber += 1
			if not line:
				return Char(False, self.lineNumber)
			else:
				self.line = deque(line)
		
		if len(self.line) > 0:
			char = Char(self.line.popleft(), self.lineNumber)
			return char


		
