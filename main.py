from ply import lex, yacc

# Define lexer tokens
tokens = (
    'IDENTIFIER',
    'NUMBER',
    'STRING',
    'OPERATOR',
    'PRINT',
    'LPAREN',
    'RPAREN',
    'COMMA',
    'EQUALS',
)

# Define regular expressions for lexer tokens
t_OPERATOR = r'[-+*/%=<>&|^~]'
t_PRINT = r'print'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r','
t_EQUALS = r'='
t_ignore = ' \t\r\n'


def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'"[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\''
    t.value = t.value[1:-1]  # Remove quotes
    return t


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


# Define grammar rules
def p_program(p):
    '''program : statement_list'''
    p[0] = p[1]


def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_statement(p):
    '''statement : assignment
                 | expression
                 | print_statement'''
    p[0] = p[1]


def p_assignment(p):
    'assignment : IDENTIFIER EQUALS expression'
    p[0] = ('assignment', p[1], p[3])


def p_expression(p):
    '''expression : NUMBER
                  | STRING
                  | IDENTIFIER
                  | expression OPERATOR expression
                  | LPAREN expression RPAREN'''
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = (p[2], p[1], p[3])


def p_print_statement(p):
    'print_statement : PRINT expression_list'
    p[0] = ('print', p[2])


def p_expression_list(p):
    '''expression_list : expression
                       | expression_list COMMA expression'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_error(p):
    print("Syntax error")


parser = yacc.yacc()


# Define tokenize function
def tokenize(code):
    lexer.input(code)
    tokens = []
    for token in lexer:
        tokens.append((token.type, token.value))
    return tokens


# Define parse function
def parse(code):
    return parser.parse(code)


if __name__ == "__main__":
    code = """
    x = 10
    y = 5
    print(x + y)
    """
    tokens = tokenize(code)
    print("Tokens:", tokens)

    parsed_code = parse(code)
    print("Parsed code:", parsed_code)
