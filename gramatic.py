import ply.yacc as yacc
import ply.lex as lex

tokens = (
    'NAME',
    'EQUALS',
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
)

# Regular expression rules for simple tokens
t_PLUS = r'\+'
t_EQUALS = r'\='
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NAME= r'[a-zA-Z_][a-zA-Z0-9_]*'

# A regular expression rule with some action code
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    #t.lexer.lineno += len(t.value)
    t.lexer.lineno += t.value.count("\n")
    #return t  # or not


# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'


# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()


#literals = ['+', '-', '*', '/']
#precedence = (
#    ('nonassoc', 'MENQUE', 'MAYQUE'),
#     ('left', 'MAS', 'MENOS'),
#     ('left', 'POR', 'DIVIDIDO'),
#     ('right', 'UNAMINUS')
# )

#----------------------------------------------------------------
precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    )
def p_statement_assign(t):
    'statement : NAME EQUALS expression'
    names[t[1]] = t[3]
def p_statement_expr(t):
    'statement : expression'
    print(t[1])
def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'
    t[0] = -t[2]
def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]
def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]
def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]
def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]
def p_expression_term(p):
    'expression : term'
    p[0] = p[1]
def p_expression_group(t):
    'expression : LPAREN expression RPAREN'
    t[0] = t[2]
def p_term_factor(p):
    'term : factor'
    p[0] = p[1]
def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]
def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]
# Error rule for syntax errors
def p_error(p):
    print(p)
    print("Error sintáctico en '%s'" % p.value)
names = { }
def p_expression_name(t):
    'expression : NAME'
    try:
        t[0] = names[t[1]]
    except LookupError:
        print("Undefined name '%s'" % t[1])
        t[0] = 0
# Build the parser
parser = yacc.yacc()