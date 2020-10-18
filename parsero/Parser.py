from lexico.lexico import *
from errorHandler import *
from parsero.parseResult import *
####################################
# PARSER
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

    def factor(self):
        res = ParseResult()
        token = self.current_token

        if token.type in (T_SUMA, T_RESTA):
            res.register(self.move())
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(token, factor))

        elif token.type in (T_ENTERO, T_DECIMAL):
            res.register(self.move())
            return res.success(NumberNode(token))

        elif token.type == T_PARENTIZQ:
            res.register(self.move())
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_token.type == T_PARENTDER:
                res.register(self.move())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end,"Expected ')'"))
        return res.failure(InvalidSyntaxError(token.pos_start, token.pos_end,"Expected ENTERO or DECIMAL"))

    def term(self):
        return self.bin_operation(self.factor,(T_MULTIPLICA,T_DIVIDE))
    def expr(self):
        return self.bin_operation(self.term, (T_SUMA, T_RESTA))

    def bin_operation(self,func,ops):
        res = ParseResult()
        left = res.register(func())
        if res.error: return res

        while self.current_token.type in ops:
            op_token = self.current_token
            res.register(self.move())
            right = res.register(func())
            if res.error: return res

            left = BinOpNode(left, op_token, right)
        return res.success(left)