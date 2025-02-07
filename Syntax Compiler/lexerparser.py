import ply.lex as lex
import ply.yacc as yacc

# List of token names
tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'IF',
    'WHILE',
    'FOR',
    'THEN',
    'ELSE',
    'DO',
    'SEMICOLON',
    'LT',        # Less than
    'GT',        # Greater than
    'LE',        # Less than or equal
    'GE',        # Greater than or equal
    'EQ',        # Equal
    'NE',        # Not equal
    'IN', 'RANGE', 'ID',
)

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_IF      = r'if'
t_FOR     = r'for'
t_WHILE   = r'while'
t_THEN    = r'then'
t_ELSE    = r'else'
t_DO      = r'do'
t_SEMICOLON = r';'
t_LT      = r'<'
t_GT      = r'>'
t_LE      = r'<='
t_GE      = r'>='
t_EQ      = r'=='
t_NE      = r'!='
t_IN = r'in'
t_RANGE = r'range'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in {'if', 'while', 'for', 'then', 'else', 'do', 'in', 'range'}:
        t.type = t.value.upper()
    return t


# A regular expression rule for NUMBER
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule to track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignore spaces and tabs
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Precedence rules
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'LT', 'GT', 'LE', 'GE', 'EQ', 'NE'),
)

# Grammar rules
def p_program(p):
    '''program : statement'''
    p[0] = p[1]

def p_statement(p):
    '''statement : if_statement
                | while_statement
                | for_statement
                | expr_statement'''
    p[0] = p[1]

def p_if_statement(p):
    'if_statement : IF LPAREN expression RPAREN THEN statement ELSE statement'
    if p[3]:
        p[0] = p[6]
    else:
        p[0] = p[8]

def p_while_statement(p):
    'while_statement : WHILE LPAREN expression RPAREN DO statement'
    max_iterations = 10
    iteration_count = 0
    results = []
    while p[3] and iteration_count < max_iterations:
        result = p[6]
        results.append(result)
        iteration_count += 1
    p[0] = results

def p_for_statement(p):
    'for_statement : FOR ID IN RANGE LPAREN NUMBER RPAREN DO statement'
    try:
        stop = p[6]
        results = []
        for i in range(min(stop, 10)): 
            results.append(p[9])
        p[0] = results
    except Exception as e:
        print(f"For loop error: {str(e)}")
        p[0] = None

def p_for_init(p):
    '''for_init : expression'''
    p[0] = p[1]

def p_for_update(p):
    '''for_update : expression'''
    p[0] = p[1]

def p_expr_statement(p):
    'expr_statement : expression'
    p[0] = p[1]

def p_expression_binop(p):
    '''expression : expression PLUS expression
                 | expression MINUS expression
                 | expression TIMES expression
                 | expression DIVIDE expression
                 | expression LT expression
                 | expression GT expression
                 | expression LE expression
                 | expression GE expression
                 | expression EQ expression
                 | expression NE expression'''
    if p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == '==':
        p[0] = p[1] == p[3]
    elif p[2] == '!=':
        p[0] = p[1] != p[3]

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

# Build the parser
parser = yacc.yacc()

# Test the parser
if __name__ == "__main__":
    while True:
        try:
            s = input('calc > ')
        except EOFError:
            break
        if not s:
            continue
        result = parser.parse(s)
        print(result)

# if (5 > 3) then 1 else 0
# if (10 == 10) then 100 else 200
# if (2 + 2 == 5) then 1 else 0
#if (2 + 3 > 4) then 1 + 2 else 3 + 4

# while (1 < 5) do 42
# while (1 == 1) do 100
# while (10 > 0) do 7
#while (5 * 2 > 3) do 10 + 5

# for x in range(5) do 1
# for i in range(3) do 42
# for count in range(4) do 100
#for x in range(2) do 3 * 4