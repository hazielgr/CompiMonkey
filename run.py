from parsero.Parser import *
from interprete.Interpreter import *
from interprete.Contexto import *
from interprete.TablaDeSimbolos import *
tabla_simbolos_global = TablaDeSimbolos()
tabla_simbolos_global.set("null",Numero.null)
tabla_simbolos_global.set("no",Numero.false)
tabla_simbolos_global.set("si",Numero.true)
def run(fn,txt):
    ##########################################################
    # Analisis de TOkens
    #########################################################
    Lexer = Lexico(fn,txt)
    tokens, error = Lexer.make_tokens()
    if error: return None, error
    ##########################################################
    # Parser
    #########################################################
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None,ast.error
    ##########################################################
    # Interprete
    #########################################################
    interprete = Interpreter()
    contexto = Context('<programa>')
    contexto.symbol_table = tabla_simbolos_global
    interpre_sol= interprete.visit(ast.node,contexto)
    return interpre_sol.value,interpre_sol.error
while True:
    txt = input('test -> ')
    result, error = run('<stdin>', txt)

    if error: print(error.as_string())
    else: print(result)