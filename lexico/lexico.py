from errorHandler import *
import string

LETRAS = string.ascii_letters
DIGITOS = '0123456789'
LETRAS_DIGITOS = LETRAS + DIGITOS
##################################
# POSICION
# La clase Position, sirve para llevar la posicion del cursor y moverlo
##################################
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

###############################
# TOKENS
# Se definen tokens conocidos
###############################
T_ENTERO       =       'ENTERO'
T_DECIMAL      =       'DECIMAL'
T_SUMA         =       'SUMA'
T_RESTA        =       'RESTA'
T_MULTIPLICA   =       'MULTIPLICA'
T_DIVIDE       =       'DIVIDE'
T_PARENTIZQ    =       'PARENTIZQ'
T_PARENTDER    =       'PARENTDER'
T_EOF          =       'EOF'
T_IDENTIFICADOR=       'IDENTIFICADOR'
T_IGUAL        =       'EQ'
T_KEYWORD      =       'KEYWORD'
T_POW		   =       'POW'


KEYWORDS = [
    'VAR'
]
# En esta clase token, se crean los tokens, con su tipo, su valor y se les pasa su posicion de inicio y final
class Token:
    def __init__(self,type_, value=None, pos_start=None, pos_end=None):
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

###########################################
# ANALIZADOR LEXICO
###########################################
# La clase Lexico inicia el analizador del archivo y crea los tokens
class Lexico:
    # Mantenemos guardado la posicion y el character
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
            elif self.current_char in DIGITOS:
                tokens.append(self.make_Number())
            elif self.current_char in LETRAS:
                tokens.append(self.make_identifier())
            elif self.current_char == '+':
                tokens.append(Token(T_SUMA,pos_start=self.pos))
                self.move()
            elif self.current_char == '-':
                tokens.append(Token(T_RESTA,pos_start=self.pos))
                self.move()
            elif self.current_char == '*':
                tokens.append(Token(T_MULTIPLICA,pos_start=self.pos))
                self.move()
            elif self.current_char == '/':
                tokens.append(Token(T_DIVIDE,pos_start=self.pos))
                self.move()
            elif self.current_char == '=':
                tokens.append(Token(T_IGUAL,pos_start=self.pos))
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
            else:
                pos_start= self.pos.copy()
                character=self.current_char
                self.move()
                return [],IllegalCharacError(pos_start,self.pos,"'"+ character+ "'")

        tokens.append(Token(T_EOF, pos_start=self.pos))
        return tokens,None

    def make_Number(self):
        # mantenemos numero en formato string
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()
        while self.current_char!=None and self.current_char in DIGITOS + '.':
            if self.current_char == '.':
                if dot_count == 1: break
                dot_count+=1
            num_str += self.current_char
            self.move()
        if dot_count == 0:
            return Token(T_ENTERO, int(num_str),pos_start, self.pos)
        else:
            return Token(T_DECIMAL, float(num_str),pos_start,self.pos)

    def make_identifier(self):
        id_string = ''
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in LETRAS_DIGITOS + '_':
            id_string += self.current_char
            self.move()

        token_type = T_KEYWORD if id_string in KEYWORDS else T_IDENTIFICADOR
        return Token(token_type,id_string,pos_start,self.pos)


######################
# Tipos de nodos
######################
class NumberNode:
    def __init__(self,token):
        self.token=token
        self.pos_start= self.token.pos_start
        self.pos_end= self.token.pos_end

    def __repr__(self):
        return f'{self.token}'

class varAccessNode:
    def __init__(self, var_name_token):
        self.var_name_token = var_name_token
        self.pos_start = self.var_name_token.pos_start
        self.pos_end = self.var_name_token.pos_end

class varAssignNode:
    def __init__(self, var_name_token, value_node):
        self.var_name_token = var_name_token
        self.value_node = value_node
        self.pos_start = self.var_name_token.pos_start
        self.pos_end = self.value_node.pos_end

class BinOpNode:
    def __init__(self,left_node,op_token,right_node):
        self.left_node=left_node
        self.op_token=op_token
        self.right_node=right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end =self.right_node.pos_end
    def __repr__(self):
        return f'({self.left_node},{self.op_token},{self.right_node})'

class UnaryOpNode:
    def __init__(self,op_token,node):
        self.op_token = op_token
        self.node = node
        self.pos_start = self.op_token.pos_start
        self.pos_end = node.pos_end

    def __repr__(self):
        return f'({self.op_token}, {self.node})'

