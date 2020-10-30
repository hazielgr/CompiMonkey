from errores.ErrorHandler import *
import string
##########################################################
# Constantes: usadas en el analizador lexico
#########################################################
MINUSCULA = string.ascii_lowercase
LETRAS = string.ascii_letters
DIGITOS = '0123456789'
SPECIAL = '@ $ ?'
LETRAS_SPECIALES = LETRAS + SPECIAL
##########################################################
# Clase Position: lleva registro de cual charac lee
#########################################################
class Position:
    def __init__(self, idx, line, column, fileName,fileContent):
        self.idx= idx
        self.ln= line
        self.col= column
        self.fn= fileName
        self.ftxt= fileContent
    def move(self, current_char=None):
        self.idx +=1
        self.col +=1
        if current_char == '\n':
            self.ln +=1
            self.col =0
        return self
    def copy(self):
        return Position(self.idx,self.ln,self.col,self.fn,self.ftxt)
##########################################################
# Constantes Tokens: Creamos los tokens
#########################################################
T_ENTERO       =       'ENTERO'
T_STRING       =       'STRING'
T_DECIMAL      =       'DECIMAL'
T_SUMA         =       'SUMA'
T_MENOS        =       'MENOS'
T_MULTIPLICA   =       'MULTIPLICA'
T_DIVIDE       =       'DIVIDE'
T_PARENTIZQ    =       'PARENTIZQ'
T_PARENTDER    =       'PARENTDER'
T_RECTIZQ      =       'RECTIZQ'
T_RECTDER      =       'RECTDER'
T_EOF          =       'EOF'
T_IDENTIFICADOR=       'IDENTIFICADOR'
T_IGUAL        =       'EQ'
T_KEYWORD      =       'KEYWORD'
T_POW		   =       'POW'
T_COMP_IGUAL   =       'COMP_EQUAL'
T_COMP_NO_IGUAL=       'COMP_NOT_EQUAL'
T_COMP_MENORQUE=       'COMP_MENORQUE'
T_COMP_MAYORQUE=       'COMP_MAYORQUE'
T_COMP_MENORIGUAL=     'COMP_MENORIGUAL'
T_COMP_MAYORIGUAL=     'COMP_MAYORIGUAL'
T_NEWLINE	   =       'NEWLINE'
T_COMA         =       'COMA'
T_FLECHA	   =       'FLECHA'
T_PUNTO        =       'PUNTO'

KEYWORDS = [
    'and' , 'or' , 'not', 'if', 'else','times','for','in','until','return'
]
##########################################################
# Clase Token: Base para crear los tokens
#########################################################
class Token:
    def __init__(self, type_ , value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value
        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.move()
        if pos_end:
            self.pos_end = pos_end.copy()
    def matches(self,type_,value):
        return  self.type == type_ and self.value == value
    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'
##########################################################
# Clase Lexico: Realiza el analisis Lexico, asigna los tokens
#########################################################
class Lexico:
    def __init__(self,fn,text):
        self.fn = fn
        self.text = text
        self.pos = Position(-1,0,-1,fn,text)
        self.current_char= None
        self.move()
    def move(self):
        self.pos.move(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in ' \t':
                self.move()
            elif self.current_char in ';\n':
                tokens.append(Token(T_NEWLINE, pos_start=self.pos))
                self.move()
            elif self.current_char in DIGITOS:
                tokens.append(self.make_numero())
            elif self.current_char in MINUSCULA:
                tokens.append(self.make_identificador())
            elif self.current_char == '"':
                tokens.append(self.make_string())
            elif self.current_char == '+':
                tokens.append(Token(T_SUMA,pos_start=self.pos))
                self.move()
            elif self.current_char == '-':
                tokens.append(self.make_minus_or_arrow())
            elif self.current_char == '*':
                tokens.append(Token(T_MULTIPLICA,pos_start=self.pos))
                self.move()
            elif self.current_char == '.':
                tokens.append(Token(T_PUNTO,pos_start=self.pos))
                self.move()
            elif self.current_char == '/':
                tokens.append(Token(T_DIVIDE,pos_start=self.pos))
                self.move()
            elif self.current_char == '^':
                tokens.append(Token(T_POW, pos_start=self.pos))
                self.move()
            elif self.current_char == '(':
                tokens.append(Token(T_PARENTIZQ,pos_start=self.pos))
                self.move()
            elif self.current_char == ')':
                tokens.append(Token(T_PARENTDER,pos_start=self.pos))
                self.move()
            elif self.current_char == '[':
                tokens.append(Token(T_RECTIZQ, pos_start=self.pos))
                self.move()
            elif self.current_char == ']':
                tokens.append(Token(T_RECTDER, pos_start=self.pos))
                self.move()
            elif self.current_char == '!':
                token, error = self.make_no_igual()
                if error: return [], error
                tokens.append(token)
            elif self.current_char == '=':
                tokens.append(self.make_igual())
            elif self.current_char == '<':
                tokens.append(self.make_menor_que())
            elif self.current_char == '>':
                tokens.append(self.make_mayor_que())
            elif self.current_char == ',':
                tokens.append(Token(T_COMA, pos_start=self.pos))
                self.move()
            else:
                pos_start= self.pos.copy()
                character=self.current_char
                self.move()
                return [],IllegalCharacError(pos_start,self.pos,"'"+ character+ "'" + " O quitar la mayuscula al inicio")
        tokens.append(Token(T_EOF, pos_start=self.pos))
        return tokens,None

    def make_numero(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()
        while self.current_char!=None and self.current_char in DIGITOS + '.':
            if self.current_char == '.':
                if dot_count==1: break
                dot_count+=1
            num_str += self.current_char
            self.move()
        if dot_count == 0:
            return Token(T_ENTERO, int(num_str),pos_start, self.pos)
        else:
            return Token(T_DECIMAL, float(num_str),pos_start,self.pos)

    def make_identificador(self):
        id_string = ''
        pos_start = self.pos.copy()
        while self.current_char != None and self.current_char in LETRAS_SPECIALES + '_':
            id_string += self.current_char
            self.move()
        token_type = T_KEYWORD if id_string in KEYWORDS else T_IDENTIFICADOR
        return Token(token_type,id_string,pos_start,self.pos)

    def make_string(self):
        string = ''
        pos_start = self.pos.copy()
        escape_char = False
        self.move()
        escape_characters = {
            'n': '\n',
            't': '\t'
        }
        while self.current_char != None and (self.current_char != '"' or escape_char):
            if escape_char:
                string += escape_characters.get(self.current_char, self.current_char)
            else:
                if self.current_char == '\\':
                    escape_char= True
                else:
                    string += self.current_char
            self.move()
            escape_char=False
        self.move()
        return Token(T_STRING, string, pos_start, self.pos)

    def make_minus_or_arrow(self):
        token_type = T_MENOS
        pos_start = self.pos.copy()
        self.move()
        if self.current_char == '>':
            self.move()
            token_type = T_FLECHA
        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def make_no_igual(self):
        pos_start = self.pos.copy()
        self.move()
        if self.current_char == '=':
            self.move()
            return Token(T_COMP_NO_IGUAL, pos_start=pos_start, pos_end=self.pos), None
        self.move()
        return None, ExpectedCharacError(pos_start, self.pos, "'=' (after '!')")

    def make_igual(self):
        token_type = T_IGUAL
        pos_start = self.pos.copy()
        self.move()
        if self.current_char == '=':
            self.move()
            token_type = T_COMP_IGUAL
        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def make_menor_que(self):
        token_type = T_COMP_MENORQUE
        pos_start = self.pos.copy()
        self.move()
        if self.current_char == '=':
            self.move()
            token_type = T_COMP_MENORIGUAL
        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def make_mayor_que(self):
        token_type = T_COMP_MAYORQUE
        pos_start = self.pos.copy()
        self.move()
        if self.current_char == '=':
            self.move()
            token_type = T_COMP_MAYORIGUAL
        return Token(token_type, pos_start=pos_start, pos_end=self.pos)
##########################################################
# Clase NumberNode: Tipo de nodo para numeros
#########################################################
class NumberNode:
    def __init__(self,token):
        self.token=token
        self.pos_start= self.token.pos_start
        self.pos_end= self.token.pos_end
    def __repr__(self):
        return f'{self.token}'
##########################################################
# Clase StringNode: Tipo de nodo para strings
#########################################################
class StringNode:
    def __init__(self,token):
        self.token=token
        self.pos_start= self.token.pos_start
        self.pos_end= self.token.pos_end
    def __repr__(self):
        return f'{self.token}'
##########################################################
# Clase ListaNode: Tipo de nodo para listas
#########################################################
class ListNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes
        self.pos_start = pos_start
        self.pos_end = pos_end
##########################################################
# Clase varAccessNode: Tipo de nodo para acceso a variables
#########################################################
class VarAccessNode:
    def __init__(self, var_name_token):
        self.var_name_token = var_name_token
        self.pos_start = self.var_name_token.pos_start
        self.pos_end = self.var_name_token.pos_end
##########################################################
# Clase varAssignNode: Tipo de nodo para su asignacion
#########################################################
class VarAssignNode:
    def __init__(self, var_name_token, value_node):
        self.var_name_token = var_name_token
        self.value_node = value_node
        self.pos_start = self.var_name_token.pos_start
        self.pos_end = self.value_node.pos_end
##########################################################
# Clase BinOpNode: Tipo de nodo para operaciones binarias
#########################################################
class BinOpNode:
    def __init__(self,left_node,op_token,right_node):
        self.left_node=left_node
        self.op_token=op_token
        self.right_node=right_node
        self.pos_start = self.left_node.pos_start
        self.pos_end =self.right_node.pos_end
    def __repr__(self):
        return f'({self.left_node},{self.op_token},{self.right_node})'
##########################################################
# Clase UnaryOpNode: Tipo de nodo para operaciones unarias
#########################################################
class UnaryOpNode:
    def __init__(self,op_token,node):
        self.op_token = op_token
        self.node = node
        self.pos_start = self.op_token.pos_start
        self.pos_end = node.pos_end
    def __repr__(self):
        return f'({self.op_token}, {self.node})'
##########################################################
# Clase CallNode: Tipo de Nodo para call
#########################################################
class CallNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes
        self.pos_start = self.node_to_call.pos_start
        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[len(self.arg_nodes) - 1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end
##########################################################
# Clase IfNode: Tipo de Nodo para if
#########################################################
class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case
        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[len(self.cases) - 1][0]).pos_end

##########################################################
# Clase ForNode: Tipo de Nodo para for
#########################################################
class ForNode:
    def __init__(self, var_name_token, start_value_node, end_value_node, body_node):
        self.var_name_token = var_name_token
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.body_node = body_node
        self.pos_start = self.var_name_token.pos_start
        self.pos_end = self.body_node.pos_end
##########################################################
# Clase UntilNode: Tipo de Nodo para until
#########################################################
class UntilNode:
    def __init__(self, condition_node, body_node):
        self.condition_node = condition_node
        self.body_node = body_node
        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end
##########################################################
# Clase ReturnNode: Tipo de Nodo para return
#########################################################
class ReturnNode:
  def __init__(self, node_to_return, pos_start, pos_end):
    self.node_to_return = node_to_return
    self.pos_start = pos_start
    self.pos_end = pos_end
##########################################################
# Clase FuncDefNode: Tipo de Nodo para definicion de funciones
#########################################################
class FuncDefNode:
  def __init__(self, var_name_token, arg_name_tokens, body_node):
    self.var_name_token = var_name_token
    self.arg_name_tokens = arg_name_tokens
    self.body_node = body_node
    if self.var_name_token:
      self.pos_start = self.var_name_token.pos_start
    elif len(self.arg_name_tokens) > 0:
      self.pos_start = self.arg_name_toks[0].pos_start
    else:
      self.pos_start = self.body_node.pos_start
    self.pos_end = self.body_node.pos_end