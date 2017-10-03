# Antonio Filho
# Diego Carvalho

import sys
import string

from IO import IO
from classes.token import Token

# Símbolos aceitos e palavras reservadas.

dictionary = ['(', ')', '{', '}', ',', ';', '+', '-', '*', '/', ' ', '\n', '\t']
words = ['int', 'main', 'float', 'if', 'else', 'while', 'read', 'print']
delimiters = [' ', '(', ')', '{', '}']
tokens = []
program = []


def addToken(token):
    program.append(token.lexical)
    tokens.append(token)


# Automato

def lexicalAnalyzer(char, file):
    if char.char == "=":
        if file.buffer[0].char == '=':
            token = Token("==", "EQ", char.line)
            addToken(token)
            char = file.getNextChar()
        else:
            token = Token(char.char, "ATTR", char.line)
            addToken(token)

    elif char.char == "!":
        if file.buffer[0].char == '=':
            token = Token("!=", "NE", char.line)
            addToken(token)
            char = file.getNextChar()

    elif char.char == ">":
        if file.buffer[0].char == '=':
            token = Token(">=", "GE", char.line)
            addToken(token)
            char = file.getNextChar()
        else:
            token = Token(char.char, "GT", char.line)
            addToken(token)

    elif char.char == "<":
        if file.buffer[0].char == '=':
            token = Token("<=", "LE", char.line)
            addToken(token)
            char = file.getNextChar()
        else:
            token = Token(char.char, "LT", char.line)
            addToken(token)

    elif char.char == "&":
        if file.buffer[0].char == '&':
            token = Token("&&", "AND", char.line)
            addToken(token)
            char = file.getNextChar()

    elif char.char == "|":
        if file.buffer[0].char == '|':
            token = Token("||", "OR", char.line)
            addToken(token)
            char = file.getNextChar()

    elif char.char == ";":
        token = Token(char.char, "PCOMMA", char.line)
        addToken(token)

    elif char.char == ",":
        token = Token(char.char, "COMMA", char.line)
        addToken(token)

    elif char.char == "}":
        token = Token(char.char, "RBRACE", char.line)
        addToken(token)

    elif char.char == "{":
        token = Token(char.char, "LBRACE", char.line)
        addToken(token)

    elif char.char == ")":
        token = Token(char.char, "RBRACKET", char.line)
        addToken(token)

    elif char.char == "(":
        token = Token(char.char, "LBRACKET", char.line)
        addToken(token)

    elif char.char == "+":
        token = Token(char.char, "PLUS", char.line)
        addToken(token)

    elif char.char == "-":
        token = Token(char.char, "MINUS", char.line)
        addToken(token)

    elif char.char == "*":
        token = Token(char.char, "MULT", char.line)
        addToken(token)

    elif char.char == "/":
        token = Token(char.char, "DIV", char.line)
        addToken(token)


    elif char.char in string.ascii_lowercase or char.char \
            in string.ascii_uppercase:
        newWord = char.char
        while file.buffer[0].char in string.ascii_lowercase or file.buffer[0].char in string.ascii_uppercase or \
                        file.buffer[0].char in string.digits:
            char = file.getNextChar()
            newWord = newWord + char.char
        if newWord in words:
            token = Token(newWord, str.upper(newWord), char.line)
        else:
            token = Token(newWord, "ID", char.line)
        addToken(token)

    elif char.char in string.digits:
        newWord = char.char
        int_avaiable = True
        while file.buffer[0].char in string.digits or file.buffer[0].char == ".":
            char = file.getNextChar()
            newWord = newWord + char.char
            if char.char == ".":
                char = file.getNextChar()
                newWord = newWord + char.char
                while file.buffer[0].char in string.digits:
                    char = file.getNextChar()
                    newWord = newWord + char.char
                token = Token(newWord, "FLOAT_CONST", char.line)
                int_avaiable = False
        if int_avaiable:
            token = Token(newWord, "INTEGER_CONST", char.line)
        addToken(token)


# Get tokens out
def getOut():
    return tokens, program


# Run AnalisadorLexico

def run():

    file = IO('main.c')
    char = file.getNextChar()
    while (char.char != False):
        lexicalAnalyzer(char, file)
        char = file.getNextChar()

    # file_out = open("out.txt", 'w')
    # file_out.write(" ".join(program))
