from lexico.lexico import *
from errorHandler import *
from parsero.parseResult import *
####################################
# PARSER
# Parser que se desplza por los tokens, dependiendo del tipo de gramatica, hace las operaciones
####################################
class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.token_idx = -1
        self.move()

    def move(self,):
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
        return self.current_token

    def parse(self):
        res= self.expr()
        if not res.error and self.current_token.type != T_EOF:
            return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end,"Expected '+', '-', '*' or '/'"))
        return res

#################### Definiendo Expresiones #################################################333

    def atom(self):
        res = ParseResult()
        token = self.current_token

        if token.type in (T_ENTERO, T_DECIMAL):
            res.register_move()
            self.move()
            return res.success(NumberNode(token))

        elif token.type == T_IDENTIFICADOR:
            res.register_move()
            self.move()
            return res.success(varAccessNode(token))

        elif token.type == T_PARENTIZQ:
            res.register_move()
            self.move()
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_token.type == T_PARENTDER:
                res.register_move()
                self.move()
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end,"Expected ')'"))
        return res.failure(InvalidSyntaxError(token.pos_start, token.pos_end,"Expected int, float, identifier, '+', '-' or '('"))

    def power(self):
        return self.bin_operation(self.atom, (T_POW,), self.factor)

    def factor(self):
        res = ParseResult()
        token = self.current_token

        if token.type in (T_SUMA, T_RESTA):
            res.register_move()
            self.move()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(token, factor))

        return self.power()

    def term(self):
        return self.bin_operation(self.factor,(T_MULTIPLICA,T_DIVIDE))
    def expr(self):
        res = ParseResult()
        # if self.current_token.matches(T_KEYWORD,'VAR'):
        # res.register(self.move())
        # if self.current_token.type!= T_IDENTIFICADOR:
        # return res.failure(InvalidSyntaxError( self.current_token.pos_start, self.current_token.pos_end, "Se esperaba un idenficador"))

        if self.current_token.type == T_IDENTIFICADOR:
            var_name = self.current_token
            res.register_move()
            self.move()

            if self.current_token.type != T_IGUAL:
                return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, "Expected ' = "))
            res.register_move()
            self.move()

            expr = res.register(self.expr())
            if res.error: return res
            return res.success(varAssignNode(var_name, expr))

        node = res.register(self.bin_operation(self.term, (T_SUMA, T_RESTA)))

        if res.error:
            return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end,"Expected int, float, identifier, '+', '-' or '('"))
        return res.success(node)

    def bin_operation(self, func_a, ops, func_b=None):
        if func_b == None : func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res

        while self.current_token.type in ops:
            op_token = self.current_token
            res.register_move()
            self.move()
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op_token, right)

        return res.success(left)