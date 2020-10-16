from Parser import *
from lexico import Lexico

def run(fn,txt):
    ################################################\
    #Analisis Tokens
    Lexer = Lexico(fn,txt)
    tokens, error = Lexer.make_tokens()
    if error: return None, error
    ################################################
    #Parser
    parser = Parser(tokens)
    ast = parser.parse()
    return ast.node, ast.error
    ###################################################

while True:
    txt = input('test -> ')
    result, error = run('<stdin>', txt)

    if error: print(error.as_string())
    else: print(result)