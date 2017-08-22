import sys
import string

from IO import IO
from Token import Token


dictionary = ['(', ')', '{', '}', ',', ';', '+', '-', '*', '/', ' ', '\n', '\t']
words = ['int', 'main', 'float', 'if', 'else', 'while', 'read', 'print']
tokens = []


def addToken(token):
	if len(tokens) > 0:
		for t in tokens:
			if token.lexical == t.lexical:
				t.setLine(token.line[0])
				return True
	tokens.append(token)


def lexicalAnalyzer(char, file):
	if char.char == "=":
		if file.buffer[0].char == '=':
			token = Token("==", "EQ", char.line )
			addToken(token)
			char = file.getNextChar()
		else:
			token = Token(char.char , "ATTR", char.line )
			addToken(token)

	elif char.char == "!":
		if file.buffer[0].char == '=':
			token = Token("!=", "NE", char.line )
			addToken(token)
			char = file.getNextChar()
		elif file.buffer[0].char == '!':
			token = Token("!!", "OR", char.line )
			addToken(token)
			char = file.getNextChar()


	elif char.char == ">":
		if file.buffer[0].char == '=':
			token = Token(">=", "GE", char.line )
			addToken(token)
			char = file.getNextChar()
		else:
			token = Token(char.char , "GT", char.line )
			addToken(token)

	elif char.char == "<":
		if file.buffer[0].char == '=':
			token = Token("<=", "LE", char.line )
			addToken(token)
			char = file.getNextChar()
		else:
			token = Token(char.char , "LT", char.line )
			addToken(token)

	elif char.char == "&":
		if file.buffer[0].char == '&':
			token = Token("&&", "AND", char.line )
			addToken(token)
			char = file.getNextChar()

	elif char.char == ";":
		token = Token(char.char , "PCOMMA", char.line )
		addToken(token)

	elif char.char == ",":
		token = Token(char.char , "COMMA", char.line )
		addToken(token)

	elif char.char == "}":
		token = Token(char.char , "RBRACE", char.line )
		addToken(token)

	elif char.char == "{":
		token = Token(char.char , "LBRACE", char.line )
		addToken(token)

	elif char.char == ")":
		token = Token(char.char , "RBRACKET", char.line )
		addToken(token)

	elif char.char == "(":
		token = Token(char.char , "LBRACKET", char.line )
		addToken(token)

	elif char.char == "+":
		token = Token(char.char , "PLUS", char.line )
		addToken(token)

	elif char.char == "-":
		token = Token(char.char , "MINUS", char.line )
		addToken(token)

	elif char.char == "*":
		token = Token(char.char , "MULT", char.line )
		addToken(token)

	elif char.char == "/":
		token = Token(char.char , "DIV", char.line )
		addToken(token)

    elif char.char in string.ascii_lowercase \
            or char.char in string.ascii_uppercase:
        newWord = char.char
        while file.buffer[0].char in string.ascii_lowercase \
                or file.buffer[0].char in string.ascii_uppercase \
                or file.buffer[0].char in string.ascii_digits:
            char = file.getNextChar()
            newWord.__add__(char.char)
        if newWord in words:
            token = Token(char.char, str.upper(newWord), char.line ) 
        else:
            token = Token(char.char, "ID", char.line )
        addToken(token)

    elif char.char in string.digits:
        while file.buffer[0].char in string.digits:
            char = file.getNextChar()
        if char.char == ".":
            char = file.getNextChar()
            while file.buffer[0].char in string.digits:
                char = file.getNextChar()
            token = Token(char.char, "FLOAT_CONST", char.line )
        else:
            token = Token(char.char, "INTEGER_CONST", char.line )
        addToken(token)


if __name__ == '__main__':
	
	file = IO('main.c')
	char = file.getNextChar()
	while(char.char != False):
		lexicalAnalyzer(char, file)
		char = file.getNextChar()

	for token in tokens:
		print(token)
