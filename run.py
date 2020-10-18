from parsero.Parser import *
from interprete.interpreter import *
from interprete.contexto import *

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
    if ast.error: return None,ast.error
    ##################################################
    #Interprete
    interprete = Interpreter()
    contexto = Context('<programa>')
    interpre_sol= interprete.visit(ast.node,contexto)


    return interpre_sol.value,interpre_sol.error
    ###################################################

while True:
    txt = input('test -> ')
    result, error = run('<stdin>', txt)

    if error: print(error.as_string())
    else: print(result)