from parsero.Parser import *
from interprete.interpreter import *
from interprete.contexto import *
from interprete.tablaDeSimbolos import *

tabla_simbolos_global = tablaDeSimbolos()
tabla_simbolos_global.set("null",Numero(0))
tabla_simbolos_global.set("no",Numero(0))
tabla_simbolos_global.set("si",Numero(1))

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
    contexto.symbol_table = tabla_simbolos_global
    interpre_sol= interprete.visit(ast.node,contexto)


    return interpre_sol.value,interpre_sol.error
    ###################################################

while True:
    txt = input('test -> ')
    result, error = run('<stdin>', txt)

    if error: print(error.as_string())
    else: print(result)