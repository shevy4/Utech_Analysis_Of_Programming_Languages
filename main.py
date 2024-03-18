from ply import lex, yacc

# Define lexer tokens
tokens = (
    'identifier',
    'integer',
    'float',
    'string',
    'operator',
    'print',
    'lparen',
    'rparen',
    'comma',
    'equals',
)

# Define regular expressions for lexer tokens
t_operator = r'[-+*/%=<>&|^~]'
t_print = r'print'
t_lparen = r'\('
t_rparen = r'\)'
t_comma = r','
t_equals = r'='
t_ignore = ' \t\r\n'


def t_float(t):
    r"""\d+\.\d+"""
    t.value = float(t.value)
    return t


def t_integer(t):
    r"""\d+"""
    t.value = int(t.value)
    return t


def t_string(t):
    r""""[^"\\]*(?:\\.[^"\\]*)*"|\'[^\'\\]*(?:\\.[^\'\\]*)*\'"""
    t.value = t.value[1:-1]  # Remove quotes
    return t


def t_identifier(t):
    r"""[a-zA-Z_][a-zA-Z0-9_]*"""
    return t


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


# Define grammar rules
def p_program(p):
    """program : statement_list"""
    p[0] = p[1]


def p_statement_list(p):
    """statement_list : statement
                      | statement_list statement"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_statement(p):
    """statement : assignment
                 | expression
                 | print_statement"""
    p[0] = p[1]


def p_assignment(p):
    """assignment : identifier equals expression"""
    p[0] = ('assignment', p[1], p[3])


def p_expression(p):
    """expression : integer
                  | float
                  | string
                  | identifier
                  | expression operator expression
                  | lparen expression rparen"""
    if len(p) == 2:
        p[0] = p[1]
    elif p[1] == '(':
        p[0] = p[2]
    else:
        p[0] = (p[2], p[1], p[3])


def p_print_statement(p):
    """print_statement : print expression_list"""
    p[0] = ('print', p[2])


def p_expression_list(p):
    """expression_list : expression
                       | expression_list comma expression"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_error(p):
    print("Syntax error:", p)


parser = yacc.yacc()

# Define a symbol table to track variable declarations and scopes
symbol_table = {}


# Define a function for semantic analysis
def semantic_analysis(parsed_code):
    for statement in parsed_code:
        if statement[0] == 'assignment':
            variable_name = statement[1]
            expression = statement[2]

            # Check if the variable is already declared
            if variable_name in symbol_table:
                print(f"Semantic Error: Variable '{variable_name}' redeclaration.")
                return False

            # Perform type checking for assignment
            if isinstance(expression, tuple):
                operator, operand1, operand2 = expression
                if operator in ('+', '-', '*', '/'):
                    # Type check for arithmetic operations
                    if not (isinstance(operand1, int) and isinstance(operand2, int)):
                        print("Semantic Error: Arithmetic operations require integer operands.")
                        return False
                elif operator == '=':
                    # Type check for assignment
                    if not isinstance(operand2, (int, str)):
                        print("Semantic Error: Assignment requires compatible types.")
                        return False

            # Add variable to symbol table
            symbol_table[variable_name] = None

        elif statement[0] == 'print':
            # Perform type checking for print statements
            for expression in statement[1]:
                if isinstance(expression, str):
                    # Check if identifier exists in symbol table
                    if expression not in symbol_table:
                        print(f"Semantic Error: Identifier '{expression}' not declared.")
                        return False
                elif not isinstance(expression, (int, str)):
                    print("Semantic Error: Print statement requires compatible types.")
                    return False

    return True


# Update parse function to return None if semantic analysis fails
def parse(code):
    parsed_code = parser.parse(code)
    if parsed_code:
        if semantic_analysis(parsed_code):
            return parsed_code
        else:
            return None
    else:
        return None


# Define tokenize function
def tokenize(code):
    lexer.input(code)
    tokens = []
    for token in lexer:
        tokens.append((token.type, token.value))
    return tokens


if __name__ == "__main__":
    code = """
    variable1 = 1.5
    """
    tokens = tokenize(code)
    print("Tokens:", tokens)

    parsed_code = parse(code)
    if parsed_code:
        print("Parsed code:", parsed_code)
