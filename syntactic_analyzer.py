# coding: utf-8
import sys

import classes.ast as tree
from classes.token import Token
from classes.symbol import Symbol

# global variables
symbol_table = {}
treeRoot = None


class Token_vector:   
    def __init__(self, tokens):
        self.tokens = tokens
        self.itr = 0

    def __len__(self):
        return len(self.tokens)

    def append(self, obj):
        self.tokens.append(obj)


def print_syntactic_error(token, tk):
    print('Ocorre um erro sintático, token esperado ' + tk + ', token encontrado: ' + str(token))


def get_token(list_tokens):
    token = list_tokens.tokens[list_tokens.itr]
    return token


def get_next_token(list_tokens):
    token = list_tokens.tokens[list_tokens.itr]
    list_tokens.itr += 1
    return token

def get_token_type(list_tokens):
    global symbol_table
    return symbol_table[get_token(list_tokens).lexical].type

def get_type_num(list_tokens):
    if get_token(list_tokens).name == 'INTEGER_CONST':
        return 'INTEGER', int(get_token(list_tokens).lexical)
    elif get_token(list_tokens).name == 'FLOAT_CONST':
        return 'FLOAT', float(get_token(list_tokens).lexical)

def match(list_tokens, tk, token_type=None):
    node = None
    global symbol_table

    if get_token(list_tokens).name == tk:
        print('token reconhecido: ' + str(get_token(list_tokens)))

        if get_token(list_tokens).name in ['ID']:
            if token_type != None:
                if token_type == 'NOTYPE':
                    token_type = get_token_type(list_tokens)
                node = tree.ID(get_token(list_tokens).lexical, token_type)
                sym = Symbol(get_token(list_tokens).lexical, token_type, get_token(list_tokens).line, None)
                symbol_table[get_token(list_tokens).lexical] = sym
            elif symbol_table.get(get_token(list_tokens).lexical, False):
                symbol = symbol_table[get_token(list_tokens).lexical]
                node = tree.ID(symbol.lexical, symbol.type)
        elif get_token(list_tokens).name in ['ATTR', 'IF', 'WHILE', 'PLUS', 'MINUS', 'MULT', 'DIV', 'EQ', 'NE', 'LT', 'LE', 'GT', 'GE', 'AND', 'OR', 'READ', 'PRINT']:
            node = get_token(list_tokens)
        elif get_token(list_tokens).name in ['INTEGER_CONST', 'FLOAT_CONST']:
            token_type, token_value = get_type_num(list_tokens)
            node = tree.Num(get_token(list_tokens).lexical, token_type, token_value)

        get_next_token(list_tokens)

    else:
        print('Ocorre um erro sintático, token esperado ' + tk + ', token encontrado: ' + str(get_token(list_tokens)))
        get_next_token(list_tokens)
    return node


def program(list_tokens):
    if len(list_tokens) <= 6:
        print("Seu programa não contém a estrutura correta para a primeira linha em c")
        return
    match(list_tokens, 'INT')
    match(list_tokens, 'MAIN')
    match(list_tokens, 'LBRACKET')
    match(list_tokens, 'RBRACKET')
    match(list_tokens, 'LBRACE')
    new_token = Token('eof', 'EOF', (list_tokens.tokens[len(list_tokens.tokens) - 1].line + 1))
    list_tokens.append(new_token)

    root = tree.ASTnode('MAIN', None)
    decl_command(list_tokens, root)

    match(list_tokens, 'RBRACE')
    if get_token(list_tokens).name == 'EOF':
        match(list_tokens, 'EOF')
        print('Fim da análise sintática.')
    return root


def decl_command(list_tokens, root):
    if get_token(list_tokens).name == 'INT' or get_token(list_tokens).name == 'FLOAT':
        declaration(list_tokens, root)
        decl_command(list_tokens, root)
    elif get_token(list_tokens).name in ['LBRACE', 'ID', 'IF', 'WHILE', 'READ', 'PRINT']:
        command(list_tokens, root)
        decl_command(list_tokens, root)

    return None


def declaration(list_tokens, root):
    token_type = op_type(list_tokens)
    node_id = match(list_tokens, 'ID', token_type)
    decl2(list_tokens, node_id, root)


def decl2(list_tokens, node_id, root):
    if get_token(list_tokens).name == 'COMMA':
        # Adiciona id na tabela de simbolos porem n retorna nada pra tree
        match(list_tokens, 'COMMA')
        node_id = match(list_tokens, 'ID', node_id.type)
        decl2(list_tokens, node_id, root)
    elif get_token(list_tokens).name == 'PCOMMA':
        match(list_tokens, 'PCOMMA')
    elif get_token(list_tokens).name == 'ATTR':
        token_attr = match(list_tokens, 'ATTR')
        node_e = expression(list_tokens)

        # cria no e add root
        node_attr = tree.Attr(token_attr.lexical, node_id, node_e)
        root.set_children(node_attr)

        decl2(list_tokens, node_id, root)


def op_type(list_tokens):
    token_type = None
    if get_token(list_tokens).name == 'INT':
        token_type = get_token(list_tokens).name
        match(list_tokens, 'INT')
    elif get_token(list_tokens).name == 'FLOAT':
        token_type = get_token(list_tokens).name
        match(list_tokens, 'FLOAT')
    else:
        print("Ocorreu um erro sintático, token esperado INT ou FLOAT: " + str(get_token(list_tokens)))
        get_next_token(list_tokens)
    return token_type


def command(list_tokens, root):
    if get_token(list_tokens).name == 'LBRACE':
        block(list_tokens, root)
    elif get_token(list_tokens).name == 'ID':
        attribution(list_tokens, root)
    elif get_token(list_tokens).name == 'IF':
        command_if(list_tokens, root)
    elif get_token(list_tokens).name == 'WHILE':
        command_while(list_tokens, root)
    elif get_token(list_tokens).name == 'READ':
        command_read(list_tokens, root)
    elif get_token(list_tokens).name == 'PRINT':
        command_print(list_tokens, root)


def block(list_tokens, root):
    match(list_tokens, 'LBRACE')
    decl_command(list_tokens, root)
    match(list_tokens, 'RBRACE')


def attribution(list_tokens, root):
    node_id = match(list_tokens, 'ID', 'NOTYPE')
    token_attr = match(list_tokens, 'ATTR', node_id.type)
    node_e = expression(list_tokens)

    # cria no e add root
    node_attr = tree.Attr(token_attr.lexical, node_id, node_e)
    root.set_children(node_attr)

    match(list_tokens, 'PCOMMA')


def command_if(list_tokens, root):
    token_if = match(list_tokens, 'IF')
    match(list_tokens, 'LBRACKET')
    node_e = expression(list_tokens)

    # cria no
    node_if = tree.IF(token_if.lexical, node_e)

    match(list_tokens, 'RBRACKET')


    node_block = tree.ASTnode('BLOCK')
    command(list_tokens, node_block)
    node_if.set_children(node_block)

    command_else(list_tokens, node_if)

    # add root
    root.set_children(node_if)
    


def command_else(list_tokens, node_if):
    if get_token(list_tokens).name == 'ELSE':
        match(list_tokens, 'ELSE')
        node_block = tree.ASTnode('BLOCK')
        command(list_tokens, node_block)
        node_if.set_children(node_block)


def command_while(list_tokens, root):
    token_while = match(list_tokens, 'WHILE')
    match(list_tokens, 'LBRACKET')
    node_e = expression(list_tokens)

    # cria no
    node_while = tree.While(token_while.lexical, node_e)
    node_block = tree.ASTnode('BLOCK')

    match(list_tokens, 'RBRACKET')
    command(list_tokens, node_block)

    # add root
    node_while.set_children(node_block)
    root.set_children(node_while)


def command_read(list_tokens, root):
    # READ
    token_r = match(list_tokens, 'READ')
    node_id = match(list_tokens, 'ID')

    #cria no
    node = tree.Read(token_r.lexical, node_id)

    match(list_tokens, 'PCOMMA')

    # add root
    root.set_children(node)


def command_print(list_tokens, root):
    # PRINT
    token_p = match(list_tokens, 'PRINT')
    match(list_tokens, 'LBRACKET')
    node_e = expression(list_tokens)

    #cria no
    node = tree.Print(token_p.lexical, node_e)

    match(list_tokens, 'RBRACKET')
    match(list_tokens, 'PCOMMA')
    
    # add root
    root.set_children(node)


def expression(list_tokens):
    node = conjunction(list_tokens)
    node = expression_opc(list_tokens, node)
    return node


def expression_opc(list_tokens, node):
    if get_token(list_tokens).name == 'OR':
        token_or = match(list_tokens, 'OR')
        node_c = conjunction(list_tokens)

        #cria no 
        node = tree.LogicalOp(token_or.lexical, node, node_c)

        node = expression_opc(list_tokens, node)
    return node


def conjunction(list_tokens):
    node = equality(list_tokens)
    node = conjunction_opc(list_tokens, node)
    return node


def conjunction_opc(list_tokens, node):
    if get_token(list_tokens).name == 'AND':
        token_and = match(list_tokens, 'AND')
        node_e = equality(list_tokens)

        #cria no
        node = tree.LogicalOp(token_and.lexical, node, node_e)

        node = conjunction_opc(list_tokens, node)
    return  node


def equality(list_tokens):
    node = relationship(list_tokens)
    node = equality_opc(list_tokens, node)
    return node


def equality_opc(list_tokens, node):
    if get_token(list_tokens).name == 'EQ' or get_token(list_tokens).name == 'NE':
        token_op = op_equal(list_tokens)
        node_r = relationship(list_tokens)

        # cria no
        node = tree.LogicalOp(token_op.lexical, node, node_r)

        node = equality_opc(list_tokens, node)
    return node


def op_equal(list_tokens):
    token = None
    if get_token(list_tokens).name == 'EQ':
        token = match(list_tokens, 'EQ')
    elif get_token(list_tokens).name == 'NE':
        token = match(list_tokens, 'NE')
    else:
        print("Ocorreu um erro sintático, token esperado EQ ou NE: " + str(get_token(list_tokens)))
        get_next_token(list_tokens)
    return token


def relationship(list_tokens):
    node = addition(list_tokens)
    node = relationship_opc(list_tokens, node)
    return node


def relationship_opc(list_tokens, node):
    if get_token(list_tokens).name in ['LT', 'LE', 'GT', 'GE']:
        token_op = op_rel(list_tokens)
        node_r = relationship(list_tokens)

        #cria no
        node = tree.RelOp(token_op.lexical, node, node_r)

        node = relationship_opc(list_tokens, node)
    return node


def op_rel(list_tokens):
    token = None
    if get_token(list_tokens).name == 'LT':
        token = match(list_tokens, 'LT')
    elif get_token(list_tokens).name == 'LE':
        token = match(list_tokens, 'LE')
    elif get_token(list_tokens).name == 'GT':
        token = match(list_tokens, 'GT')
    elif get_token(list_tokens).name == 'GE':
        token = match(list_tokens, 'GE')
    return token


def addition(list_tokens):
    node = term(list_tokens)
    node = addition_opc(list_tokens, node)
    return node


def addition_opc(list_tokens, node):
    if get_token(list_tokens).name == 'PLUS' or get_token(list_tokens).name == 'MINUS':
        node_left = node
        token_op = op_addition(list_tokens)
        node_t = term(list_tokens)

        # cria no
        node = tree.ArithOp(token_op.lexical, node_left, node_t)

        node = addition_opc(list_tokens, node)
    return node
        


def op_addition(list_tokens):
    token = None
    if get_token(list_tokens).name == 'PLUS':
        token = match(list_tokens, 'PLUS')
    elif get_token(list_tokens).name == 'MINUS':
        token = match(list_tokens, 'MINUS')
    else:
        print("Ocorreu um erro sintático, token esperado PLUS ou MINUS: " + str(get_token(list_tokens)))
        get_next_token(list_tokens)
    return token


def term(list_tokens):
    node = factor(list_tokens)
    node = term_opc(list_tokens, node)
    return node


def term_opc(list_tokens, node):
    if get_token(list_tokens).name == 'MULT' or get_token(list_tokens).name == 'DIV':
        token_op = op_mult(list_tokens)
        node_f = factor(list_tokens)
        
        #cria no
        node = tree.ArithOp(token_op.lexical, node, node_f)

        term_opc(list_tokens, node)
    return node

    
def op_mult(list_tokens):
    token = None
    if get_token(list_tokens).name == 'MULT':
        token = match(list_tokens, 'MULT')
    elif get_token(list_tokens).name == 'DIV':
        token = match(list_tokens, 'DIV')
    else:
        print("Ocorreu um erro sintático, token esperado MULT ou DIV: " + str(get_token(list_tokens)))
        get_next_token(list_tokens)
    return token


def factor(list_tokens):
    node = None
    if get_token(list_tokens).name == 'ID':
        node = match(list_tokens, 'ID')
    elif get_token(list_tokens).name == 'INTEGER_CONST':
        node = match(list_tokens, 'INTEGER_CONST')
    elif get_token(list_tokens).name == 'FLOAT_CONST':
        node = match(list_tokens, 'FLOAT_CONST')
    elif get_token(list_tokens).name == 'LBRACKET':
        match(list_tokens, 'LBRACKET')
        node = expression(list_tokens)
        match(list_tokens, 'RBRACKET')
    return node


def getTree():
    global treeRoot
    return treeRoot


def getSymbolTable():
    global symbol_table
    return symbol_table


def run(tokens):
    global treeRoot
    list_tokens = Token_vector(tokens)
    treeRoot = program(list_tokens)