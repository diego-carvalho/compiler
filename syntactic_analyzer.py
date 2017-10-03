

from classes.token import Token


class Token_vector:   
    def __init__(self, tokens):
        self.tokens = tokens
        self.itr = 0


def print_syntactic_error(token):
    print("%s esperado na linha %d" % (token.name, int(token.line)))


def get_token(list_tokens):
    token = list_tokens.tokens[list_tokens.itr]
    return token


def get_next_token(list_tokens):
    token = list_tokens.tokens[list_tokens.itr]
    list_tokens.itr += 1
    return token


def program(list_tokens):
    if len(list_tokens) <= 6:
        print("Seu programa não contém a estrutura correta para a primeira linha em c")
        return
    token = list_tokens.pop(0)
    if token.lexical != 'INT':
        print_syntactic_error(token)
    token = list_tokens.pop(0)
    if token.lexical == 'MAIN':
        print_syntactic_error(token)
    token = list_tokens.pop(0)
    if token.lexical == 'LBRACKET':
        print_syntactic_error(token) 
    token = list_tokens.pop(0)
    if token.lexical == 'RBRACKET':
        print_syntactic_error(token) 
    token = list_tokens.pop(0)
    if token.lexical == 'LBRACE':
        print_syntactic_error(token)
    # get penultimate token in my program and verify if is equal to }
    token = list_tokens.pop(len(list_tokens) - 1)
    if token.lexical == 'RBRACE':
        print_syntactic_error(token)
    
    new_token = Token('eof', 'EOF', token.line)
    list_tokens.append(new_token)

    decl_command(list_tokens)


def decl_command(list_tokens):
    if get_token(list_tokens).lexical == 'INT' or get_token(list_tokens).lexical == 'FLOAT':
        declaration(list_tokens)
        decl_command(list_tokens)
    elif get_token(list_tokens).lexical == 'NSEI':
        command(list_tokens)
        decl_command(list_tokens)
    elif get_token(list_tokens).lexical == 'EOF':
        match(list_tokens, 'EOF')
        print('Fim da análise sintática.')


def declaration(list_tokens):
    op_type(list_tokens)
    match(list_tokens, 'ID')
    decl2(list_tokens)


def decl2(list_tokens):
    if get_token(list_tokens).lexical == 'COMMA':
        match(list_tokens, 'COMMA')
        match(list_tokens, 'ID')
        decl2(list_tokens)
    elif get_token(list_tokens).lexical == 'PCOMMA':
        match(list_tokens, 'PCOMMA')
    elif get_token(list_tokens).lexical == 'ATTR':
        match(list_tokens, 'ATTR')
        expression(list_tokens)
        decl2(list_tokens)


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
        block(list_tokens)
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
    command(list_tokens)
    match(list_tokens, 'RBRACE')


def attribution(list_tokens):
    match(list_tokens, 'ID')
    match(list_tokens, 'ATTR')
    expression(list_tokens)
    match(list_tokens, 'PCOMMA')


def command_if(list_tokens):
    match(list_tokens, 'IF')
    match(list_tokens, 'LBRACKET')
    expression(list_tokens)
    match(list_tokens, 'RBRACKET')
    command(list_tokens)
    command_else(list_tokens)


def command_else(list_tokens):
    if get_token(list_tokens).lexical == 'ELSE':
        match(list_tokens, 'ELSE')
        command(list_tokens)


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
    conjunction(list_tokens)
    expression_opc(list_tokens)


def expression_opc(list_tokens):
    if get_token(list_tokens).lexical == 'OR':
        match(list_tokens, 'OR')
        conjunction(list_tokens)
        expression_opc(list_tokens)


def conjunction(list_tokens):
    match(list_tokens, 'EQ')
    conjunction_opc(list_tokens)


def conjunction_opc(list_tokens):
    if get_token(list_tokens).lexical == 'AND':
        match(list_tokens, 'AND')
        match(list_tokens, 'EQ')
        conjunction_opc(list_tokens)


def equality(list_tokens):
    relationship(list_tokens)
    equality_opc(list_tokens)


def equality_opc(list_tokens):
    if get_token(list_tokens).lexical == 'EQ' or get_token(list_tokens).lexical == 'NE':
        op_equal(list_tokens)
        relationship(list_tokens)
        equality_opc(list_tokens)


def op_equal(list_tokens):
    if get_token(list_tokens).lexical == 'EQ':
        match(list_tokens, 'EQ')
    elif get_token(list_tokens).lexical == 'NE':
        match(list_tokens, 'NE')
    else:
        print("Ocorreu um erro sintático, token esperado EQ ou NE: " + str(get_token(list_tokens)))
        get_next_token(list_tokens)


def relationship(list_tokens):
    addition(list_tokens)
    relationship_opc(list_tokens)


def relationship_opc(list_tokens):
    if get_token(list_tokens).lexical == 'EQ' or get_token(list_tokens).lexical == 'NE':
        op_rel(list_tokens)
        relationship(list_tokens)
        relationship_opc(list_tokens)


def op_rel(list_tokens):
    if get_token(list_tokens).lexical == 'LT':
        match(list_tokens, 'LT')
    elif get_token(list_tokens).lexical == 'LE':
        match(list_tokens, 'LE')
    elif get_token(list_tokens).lexical == 'GT':
        match(list_tokens, 'GT')
    elif get_token(list_tokens).lexical == 'GE':
        match(list_tokens, 'GE')
    else:
        print("Ocorreu um erro sintático, token esperado LT, LE, GT ou GE: " + str(get_token(list_tokens)))
        get_next_token(list_tokens)


def addition(list_tokens):
    term(list_tokens)
    addition_opc(list_tokens)


def addition_opc(list_tokens):
    if get_token(list_tokens).lexical == 'PLUS' or get_token(list_tokens).lexical == 'MINUS':
        op_addition(list_tokens)
        term(list_tokens)
        addition_opc(list_tokens)


def op_addition(list_tokens):
    if get_token(list_tokens).lexical == 'PLUS':
        match(list_tokens, 'PLUS')
    elif get_token(list_tokens).lexical == 'MINUS':
        match(list_tokens, 'MINUS')
    else:
        print("Ocorreu um erro sintático, token esperado PLUS ou MINUS: " + str(get_token(list_tokens)))
        get_next_token(list_tokens)


def term(list_tokens):
    factor(list_tokens)
    term_opc(list_tokens)


def term_opc(list_tokens):
    if get_token(list_tokens).lexical == 'MULT' or get_token(list_tokens).lexical == 'DIV':
        op_mult(list_tokens)
        factor(list_tokens)
        term_opc(list_tokens)

    
def op_mult(list_tokens):
    if get_token(list_tokens).lexical == 'MULT':
        match(list_tokens, 'MULT')
    elif get_token(list_tokens).lexical == 'DIV':
        match(list_tokens, 'DIV')
    else:
        print("Ocorreu um erro sintático, token esperado MULT ou DIV: " + str(get_token(list_tokens)))
        get_next_token(list_tokens)


def factor(list_tokens):
    if get_token(list_tokens).lexical == 'ID':
        match(list_tokens, 'ID')
    if get_token(list_tokens).lexical == 'INT':
        match(list_tokens, 'INT')
    if get_token(list_tokens).lexical == 'FLOAT':
        match(list_tokens, 'FLOAT')
    if get_token(list_tokens).lexical == 'LBRACKET':
        match(list_tokens, 'LBRACKET')
        expression(list_tokens)
        match(list_tokens, 'RBRACKET')



def match(list_tokens, tk):
    if get_token(list_tokens).lexical == tk:
        print('token reconhecido: ' + str(get_token(list_tokens)))
        get_next_token(list_tokens)
    else:
        print('Ocorre um erro sintático, token esperado ' + tk + ', token encontrado: ' + str(get_token(list_tokens)))
        get_next_token(list_tokens)


def run(tokens):
    list_tokens = Token_vector(tokens)
    program(list_tokens)