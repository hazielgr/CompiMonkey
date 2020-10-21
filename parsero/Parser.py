from lexico.Lexico import *
from errores.errorHandler import *
from parsero.ParseResult import *
##########################################################
# Clase Parser: Se define la sintaxis, la gramatica como esta compuesta
#########################################################
class Parser:
    def __init__(self,tokens):
        self.tokens = tokens
        self.token_idx = -1
        self.move()
    def move(self,):
        self.token_idx += 1
        self.update_current_token()
        return self.current_token
    def update_current_token(self):
        if self.token_idx >= 0 and self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
    def parse(self):
        res = self.statements()
        if not res.error and self.current_token.type != T_EOF:
            return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end,"Expected '+', '-', '*', '/', '^', '==', '!=', '<', '>', <=', '>=', 'and' or 'or'"))
        return res
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
        elif token.matches(T_KEYWORD, 'if'):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)
        return res.failure(InvalidSyntaxError(token.pos_start, token.pos_end,"Expected int, float, identifier, '+', '-' or '('"))
    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_token.pos_start.copy()
        while self.current_token.type == T_NEWLINE:
            res.register_move()
            self.move()
        statement = res.register(self.expr())
        if res.error: return res
        statements.append(statement)
        more_statements = True
        while True:
            newline_count = 0
            while self.current_token.type == T_NEWLINE:
                res.register_move()
                self.move()
                newline_count += 1
            if newline_count == 0:
                more_statements = False
            if not more_statements: break
            statement = res.try_register(self.expr())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)
        return res.success(ListNode(statements,pos_start,self.current_token.pos_end.copy()))
    def expr(self):
        res = ParseResult()
        if self.current_token.type == T_IDENTIFICADOR:
            var_name = self.current_token
            res.register_move()
            self.move()

            if self.current_token.type != T_IGUAL:
                return res.failure(
                    InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end, "Expected ' = "))
            res.register_move()
            self.move()

            expr = res.register(self.expr())
            if res.error: return res
            return res.success(varAssignNode(var_name, expr))
        node = res.register(self.bin_operation(self.comp_expr, ((T_KEYWORD, "and"), (T_KEYWORD, 'or'))))
        if res.error:
            return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end,"Expected int, float, identifier, '+', '-' or '('"))
        return res.success(node)
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
    def arith_expr(self):
        return self.bin_operation(self.term, (T_SUMA, T_RESTA))
    def comp_expr(self):
        res = ParseResult()
        if self.current_token.matches(T_KEYWORD, 'not'):
            op_token = self.current_token
            res.register_move()
            self.move()
            node = res.register(self.comp_expr())
            if res.error: return res
            return res.success(UnaryOpNode(op_token, node))
        node = res.register(self.bin_operation(self.arith_expr, (T_COMP_IGUAL, T_COMP_NO_IGUAL, T_COMP_MENORQUE, T_COMP_MAYORQUE, T_COMP_MENORIGUAL, T_COMP_MAYORIGUAL)))
        if res.error:
            return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end,"Expected int, float, identifier, '+', '-', '(' or 'not'"))
        return res.success(node)
    def power(self):
        return self.bin_operation(self.atom, (T_POW,), self.factor)
    def bin_operation(self, func_a, ops, func_b=None):
        if func_b == None : func_b = func_a
        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res
        while self.current_token.type in ops or (self.current_token.type, self.current_token.value) in ops:
            op_token = self.current_token
            res.register_move()
            self.move()
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op_token, right)
        return res.success(left)

    def if_expr(self):
        res = ParseResult()
        cases = []
        else_case = None
        if not self.current_token.matches(T_KEYWORD, 'if'):
            return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end,f"Expected 'if'"))
        res.register_move()
        self.move()
        condition = res.register(self.expr())
        if res.error: return res
        if not self.current_token.type != T_NEWLINE:
            return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end,f"Expected 'NEWLINE'"))
        res.register_move()
        self.move()
        expr = res.register(self.expr())
        if res.error: return res
        cases.append((condition, expr))
        if self.current_token.matches(T_KEYWORD, 'ELSE'):
            res.register_move()
            self.move()
            else_case = res.register(self.expr())
            if res.error: return res
        return res.success(IfNode(cases, else_case))
