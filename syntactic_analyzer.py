# coding: utf-8


import classes.ast as tree
from classes.token import Token


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

def match(list_tokens, tk):
    node = None
    if get_token(list_tokens).lexical == tk:
        print('token reconhecido: ' + str(get_token(list_tokens)))

        if get_token(list_tokens).lexical in ['INTEGER_CONST', 'FLOAT_CONST']:
            node = tree.ASTnode(get_token(list_tokens).name, None)

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
    current_node = root

    root.set_children(decl_command(list_tokens))

    match(list_tokens, 'RBRACE')
    if get_token(list_tokens).lexical == 'EOF':
        match(list_tokens, 'EOF')
        print('Fim da análise sintática.')


def decl_command(list_tokens):
    if get_token(list_tokens).lexical == 'INT' or get_token(list_tokens).lexical == 'FLOAT':
        node_d = declaration(list_tokens)
        node_opc = decl_command(list_tokens)
        if node_opc:
            node_opc.set_children(node_d)
            node_d.set_father(node_opc)
            return node_opc
            print(node_opc)
        else:
            return node_d
            print(node_d)
    elif get_token(list_tokens).lexical in ['LBRACE', 'ID', 'IF', 'WHILE', 'READ', 'PRINT']:
        node_c = command(list_tokens)
        node_opc = decl_command(list_tokens)
        if node_opc:
            node_opc.set_children(node_c)
            node_c.set_father(node_opc)
            return node_opc
        else:
            return node_c

    return None


def declaration(list_tokens):
    op_type(list_tokens)
    node_id = match(list_tokens, 'ID')
    node_d = decl2(list_tokens)
    if node_d:
        node_d.set_children(node_id)
    if node_id:
        node_id.set_father(node_d)
    return node_d


def decl2(list_tokens):
    if get_token(list_tokens).lexical == 'COMMA':
        # Adiciona id na tabela de simbolos porem n retorna nada pra tree
        match(list_tokens, 'COMMA')
        match(list_tokens, 'ID')
        decl2(list_tokens)
    elif get_token(list_tokens).lexical == 'PCOMMA':
        match(list_tokens, 'PCOMMA')
    elif get_token(list_tokens).lexical == 'ATTR':
        node_op = match(list_tokens, 'ATTR')
        node_e = expression(list_tokens)
        decl2(list_tokens)
        if node_op:
            node = tree.Assing('Assing', node_e)
            node_op.set_children(node_e)
            node_e.set_father(node_op)
        return node_op
    return None


def op_type(list_tokens):
    if get_token(list_tokens).lexical == 'INT':
        match(list_tokens, 'INT')
    elif get_token(list_tokens).lexical == 'FLOAT':
        match(list_tokens, 'FLOAT')
    else:
        print("Ocorreu um erro sintático, token esperado INT ou FLOAT: " + str(get_token(list_tokens)))
        get_next_token(list_tokens)


def command(list_tokens):
    if get_token(list_tokens).lexical == 'LBRACE':
        node_b = block(list_tokens)
        return node_b
    if get_token(list_tokens).lexical == 'ID':
        attribution(list_tokens)
    if get_token(list_tokens).lexical == 'IF':
        command_if(list_tokens)
    if get_token(list_tokens).lexical == 'WHILE':
        command_while(list_tokens)
    if get_token(list_tokens).lexical == 'READ':
        command_read(list_tokens)
    if get_token(list_tokens).lexical == 'PRINT':
        command_print(list_tokens)


def block(list_tokens):
    match(list_tokens, 'LBRACE')
    node_decl = decl_command(list_tokens)
    match(list_tokens, 'RBRACE')
    return node_decl


def attribution(list_tokens):
    match(list_tokens, 'ID')
    match(list_tokens, 'ATTR')
    expression(list_tokens)
    match(list_tokens, 'PCOMMA')


def command_if(list_tokens):
    node_if = match(list_tokens, 'IF')
    match(list_tokens, 'LBRACKET')
    node_e = expression(list_tokens)
    match(list_tokens, 'RBRACKET')
    node_c = command(list_tokens)
    node_else = command_else(list_tokens)
    if node_else:
        node_if = tree.IF('IF', node_e, node_c, node_else, None)
    else:
        node_if = tree.IF('IF', node_e, node_c, None, None)
    return node_if


def command_else(list_tokens):
    if get_token(list_tokens).lexical == 'ELSE':
        match(list_tokens, 'ELSE')
        node_c = command(list_tokens)
        return node_c
    return None


def command_while(list_tokens):
    match(list_tokens, 'WHILE')
    match(list_tokens, 'LBRACKET')
    expression(list_tokens)
    match(list_tokens, 'RBRACKET')
    command(list_tokens)


def command_read(list_tokens):
    # READ
    match(list_tokens, 'READ')
    match(list_tokens, 'ID')
    match(list_tokens, 'PCOMMA')


def command_print(list_tokens):
    # PRINT
    match(list_tokens, 'PRINT')
    match(list_tokens, 'LBRACKET')
    expression(list_tokens)
    match(list_tokens, 'RBRACKET')
    match(list_tokens, 'PCOMMA')


def expression(list_tokens):
    node_con = conjunction(list_tokens)
    node_opc = expression_opc(list_tokens)
    if node_opc:
        node_opc.set_children(node_con)
        node_con.set_father(node_opc)
        return node_opc
    return node_con


def expression_opc(list_tokens):
    if get_token(list_tokens).lexical == 'OR':
        node = match(list_tokens, 'OR')
        node_con = conjunction(list_tokens)
        node_opc = expression_opc(list_tokens)
        if node_opc:
            node_opc.set_children(node_con)
            node_con.set_father(node_opc)
            node.set_children(node_opc)
            node_opc.set_father(node)
        else:
            node.set_children(node_con)
            node_con.set_father(node)
        return node
    return None


def conjunction(list_tokens):
    node_e = equality(list_tokens)
    node_opc = conjunction_opc(list_tokens)
    if node_opc:
        node_opc.set_children(node_e)
        node_e.set_father(node_opc)
        return node_opc
    return node_e


def conjunction_opc(list_tokens):
    if get_token(list_tokens).lexical == 'AND':
        node_op = match(list_tokens, 'AND')
        node_e = equality(list_tokens)
        node_opc = conjunction_opc(list_tokens)
        if node_opc:
            node_op.set_children(node_opc)
            node_opc.set_father(node_op)
        node_op.set_children(node_e)
        node_e.set_father(node_op)
        return node_op
    return None


def equality(list_tokens):
    node_rel = relationship(list_tokens)
    node_opc = equality_opc(list_tokens)
    if node_opc:
        node_opc.set_children(node_rel)
        node_rel.set_father(node_opc)
        return node_opc
    return node_rel


def equality_opc(list_tokens):
    if get_token(list_tokens).lexical == 'EQ' or get_token(list_tokens).lexical == 'NE':
        node_op = op_equal(list_tokens)
        node_rel = relationship(list_tokens)
        node_opc = equality_opc(list_tokens)
        if node_opc:
            node_op.set_children(node_opc)
            node_opc.set_father(node_op)
        if node_op:
            node_op.set_children(node_rel)
        if node_rel:
            node_rel.set_father(node_op)
        return node_op
    return None


def op_equal(list_tokens):
    node = None
    if get_token(list_tokens).lexical == 'EQ':
        node = match(list_tokens, 'EQ')
    elif get_token(list_tokens).lexical == 'NE':
        node = match(list_tokens, 'NE')
    else:
        print("Ocorreu um erro sintático, token esperado EQ ou NE: " + str(get_token(list_tokens)))
        get_next_token(list_tokens)
    return node


def relationship(list_tokens):
    node_add = addition(list_tokens)
    node_rel = relationship_opc(list_tokens)
    if node_rel:
        node_rel.set_children(node_add)
        node_add.set_father(node_rel)
        return node_rel
    return node_add


def relationship_opc(list_tokens):
    if get_token(list_tokens).lexical in ['LT', 'LE', 'GT', 'GE']:
        node_op = op_rel(list_tokens)
        node_rel = relationship(list_tokens)
        node_opc = relationship_opc(list_tokens)
        if node_opc:
            node_op.set_children(node_opc)
            node_opc.set_father(node_op)
        node_op.set_children(node_rel)
        node_rel.set_father(node_op)
        return node_op
    return None


def op_rel(list_tokens):
    node = None
    if get_token(list_tokens).lexical == 'LT':
        node = match(list_tokens, 'LT')
    elif get_token(list_tokens).lexical == 'LE':
        node = match(list_tokens, 'LE')
    elif get_token(list_tokens).lexical == 'GT':
        node = match(list_tokens, 'GT')
    elif get_token(list_tokens).lexical == 'GE':
        node = match(list_tokens, 'GE')
    return node


def addition(list_tokens):
    # 4 + 5
    # 4
    node_term = term(list_tokens)
    # + 5
    node_add = addition_opc(list_tokens)
    if node_add:
        node_add.set_children(node_term)
        node_term.set_father(node_add)
        return node_add
    return node_term


def addition_opc(list_tokens):
    if get_token(list_tokens).lexical == 'PLUS' or get_token(list_tokens).lexical == 'MINUS':
        # +
        node_op = op_addition(list_tokens)
        # 5
        node_term = term(list_tokens)
        node_opc = addition_opc(list_tokens)
        if node_opc:
            pass
        


def op_addition(list_tokens):
    node = None
    if get_token(list_tokens).lexical == 'PLUS':
        node = match(list_tokens, 'PLUS')
    elif get_token(list_tokens).lexical == 'MINUS':
        node = match(list_tokens, 'MINUS')
    else:
        print("Ocorreu um erro sintático, token esperado PLUS ou MINUS: " + str(get_token(list_tokens)))
        get_next_token(list_tokens)
    return node


def term(list_tokens):
    # = 4 * 5
    # 4
    node_fact = factor(list_tokens)
    # * 5
    node_term = term_opc(list_tokens)
    if node_term:
        node_term.set_children(node_fact)
        node_fact.set_father(node_term)
        return node_term
    return None


def term_opc(list_tokens):
    if get_token(list_tokens).lexical == 'MULT' or get_token(list_tokens).lexical == 'DIV':
        # *
        node_op = op_mult(list_tokens)
        # 5
        node_fact = factor(list_tokens)
        # ; -> None or / 10
        node_term = term_opc(list_tokens)
        node_fact.set_father(node_op)
        node_op.set_children(node_fact)
        if node_term:
            node_op.set_children(node_term)
            node_term.set+father(node_op)
        return node_op
    return None

    
def op_mult(list_tokens):
    node = None
    if get_token(list_tokens).lexical == 'MULT':
        node = match(list_tokens, 'MULT')
    elif get_token(list_tokens).lexical == 'DIV':
        node = match(list_tokens, 'DIV')
    else:
        print("Ocorreu um erro sintático, token esperado MULT ou DIV: " + str(get_token(list_tokens)))
        get_next_token(list_tokens)
    return node


def factor(list_tokens):
    node = None
    if get_token(list_tokens).lexical == 'ID':
        match(list_tokens, 'ID')
        # se existir ID na tabela de simbolos retorna o valor, se n acho que eh erro
    elif get_token(list_tokens).lexical == 'INTEGER_CONST':
        node = match(list_tokens, 'INTEGER_CONST')
    elif get_token(list_tokens).lexical == 'FLOAT_CONST':
        node = match(list_tokens, 'FLOAT_CONST')
    elif get_token(list_tokens).lexical == 'LBRACKET':
        #aqui preciso pegar a expressao como possivel valor
        match(list_tokens, 'LBRACKET')
        expression(list_tokens)
        match(list_tokens, 'RBRACKET')
    return node

# variables used in all program
current_node = None

def run(tokens):
    list_tokens = Token_vector(tokens)
    program(list_tokens)