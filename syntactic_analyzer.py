# coding: utf-8


import classes.ast as ast
from classes.token import Token
import sys

st = {}

class Token_vector:   
    def __init__(self, tokens):
        self.tokens = tokens
        self.itr = 0

    def __len__(self):
        return len(self.tokens)

    def append(self, obj):
        self.tokens.append(obj)


def print_syntactic_error(token, tk):
    print('Ocorre um erro sintático, token encontrado: ' + str(token) + ', token esperado: ' + str(tk.lexical))


def get_token(list_tokens):
    token = list_tokens.tokens[list_tokens.itr]
    return token


def get_next_token(list_tokens):
    token = list_tokens.tokens[list_tokens.itr]
    list_tokens.itr += 1
    return token

def match(tk):
    if get_token(list_tokens).lexical == tk:
        return True
    else:
        return False

def check(tk):
    if match(tk):
        if tk != 'EOF':
            get_next_token(list_tokens)
        print('token reconhecido: ' + str(get_token(list_tokens)))
        return True
    else:
        print_syntactic_error(tk, get_token(list_tokens))
        get_next_token(list_tokens)
        return False

def conseq_match(vec):
    for tk in vec:
        check(tk)

def program():
    if len(list_tokens) <= 6:
        print("Seu programa não contém a estrutura correta para a primeira linha em c")
        return
    check('INT')
    check('MAIN')
    check('LBRACKET')
    check('RBRACKET')
    check('LBRACE')
    new_token = Token('eof', 'EOF', (list_tokens.tokens[len(list_tokens.tokens) - 1].line + 1))
    list_tokens.append(new_token)

    main_node = ast.ASTnode('ASTnode')

    while not match('RBRACE'):
        astnode(main_node)

    check('RBRACE')
    check('EOF')
    print("AST:")

    aux_stdout = sys.stdout
    f = open('AST.xml','w')
    sys.stdout = f
    main_node.print()
    sys.stdout = aux_stdout

    f.close()

    print('Fim da análise sintática.')

    print('Tabela de símbolos:')
    print(st)

def astnode(father):
    if match('INT') or match('FLOAT') or match('ID'):
        attrNode(father,"")
    elif match('IF'):
        ifNode(father)
    elif match('WHILE'):
        whileNode(father)
    else:
        check('.')

LOP = ['EQ', 'NE', 'GE', 'GT', 'LE', 'LT', 'AND', 'OR']
AOP = ['PLUS', 'MINUS', 'MULT', 'DIV']

def attrNode(father,type):
    node = ast.ASTnode('Attr')
    father.addChildren(node)
    type = "integer"
    if match('INT'):
        check('INT')
        type = 'integer'
    elif match('FLOAT'):
        check('FLOAT')
        type = 'float'
    cnode = ast.ASTnode('Id')
    cnode.set_value(get_token(list_tokens).name)
    cnode.set_type(type)
    st[cnode.value] = (type,get_token(list_tokens).line)
    node.addChildren(cnode)
    check('ID')
    if match('ATTR'):
        check('ATTR')
        if match('ID'):
            check('ID')
        elif match('FLOAT_CONST'):
            bnode = ast.ASTnode('Num')
            bnode.set_value(get_token(list_tokens).name)
            bnode.set_type("float")
            node.addChildren(cnode)
            check('FLOAT_CONST')
        elif match('INTEGER_CONST'):
            cnode = ast.ASTnode('Num')
            cnode.set_value(get_token(list_tokens).name)
            cnode.set_type("integer")
            node.addChildren(cnode)
            check('INTEGER_CONST')

        if get_token(list_tokens).lexical in AOP:
            anode = ast.ASTnode('ArithOp')
            anode.set_value(get_token(list_tokens).name)
            node.addChildren(anode)
            check(get_token(list_tokens).lexical)
            anode.addChildren(cnode)

        if match('ID'):
            cnode = ast.ASTnode('Id')
            cnode.set_value(get_token(list_tokens).name)
            anode.addChildren(cnode)
            check('ID')
        elif match('FLOAT_CONST'):
            cnode = ast.ASTnode('Num')
            cnode.set_value(get_token(list_tokens).name)
            cnode.set_type("float")
            anode.addChildren(cnode)
            check('FLOAT_CONST')
        elif match('INTEGER_CONST'):
            cnode = ast.ASTnode('Num')
            cnode.set_value(get_token(list_tokens).name)
            cnode.set_type("integer")
            anode.addChildren(cnode)
            check('INTEGER_CONST')

    if not match('PCOMMA'):
        check('COMMA')
        attrNode(node,type)
    else:
        check('PCOMMA')

def exprNode(father):
    node = ast.ASTnode('Expr')
    father.addChildren(node)
    if get_token(list_tokens).lexical == 'ID':
        cnode = ast.ASTnode('Id')
        cnode.set_value(get_token(list_tokens).name)
        node.addChildren(cnode)
        check(get_token(list_tokens).lexical)

        if get_token(list_tokens).lexical in LOP:
            anode = ast.ASTnode('LogicalOp')
            anode.set_value(get_token(list_tokens).name)
            anode.addChildren(cnode)
            check(get_token(list_tokens).lexical)
        elif get_token(list_tokens).lexical in AOP:
            cnode = ast.ASTnode('ArithOp')
            cnode.set_value(get_token(list_tokens).name)
            node.addChildren(cnode)
            check(get_token(list_tokens).lexical)

        if get_token(list_tokens).lexical in ['INTEGER_CONST', 'FLOAT_CONST']:
            cnode = ast.ASTnode('Num')
            if get_token(list_tokens).lexical == 'INTEGER_CONST':
                cnode.set_type('integer')
            else:
                cnode.set_type('float')
            cnode.set_value(get_token(list_tokens).name)
            node.addChildren(cnode)
            check(get_token(list_tokens).lexical)
        elif get_token(list_tokens).lexical == 'ID':
            cnode = ast.ASTnode('Id')
            cnode.set_value(get_token(list_tokens).name)
            node.addChildren(cnode)
            check(get_token(list_tokens).lexical)

        anode.addChildren(cnode)
        node.addChildren(anode)

    elif match('INTEGER_CONST'):
        anode = ast.ASTnode('Num')
        anode.set_type('integer')
        anode.set_value(get_token(list_tokens).name)
        node.addChildren(anode)
        check('INTEGER_CONST')


def ifNode(father):
    node = ast.ASTnode('If')
    father.addChildren(node)
    check('IF')
    check('LBRACKET')
    exprNode(node)
    check('RBRACKET')

    check('LBRACE')
    astnode(node)
    check('RBRACE')

    if match('ELSE'):
        check('ELSE')
        check('LBRACE')
        astnode(node)
        check('RBRACE')

def whileNode(father):
    node = ast.ASTnode('While')
    father.addChildren(node)
    check('WHILE')
    check('LBRACKET')
    exprNode(node)
    check('RBRACKET')

    check('LBRACE')
    astnode(node)
    check('RBRACE')

def run(tokens):
    global list_tokens
    list_tokens = Token_vector(tokens)
    program()