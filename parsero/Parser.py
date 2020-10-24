from lexico.Lexico import *
from errores.ErrorHandler import *
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
    def reverse(self, amount=1):
        self.token_idx -= amount
        self.update_current_token()
        return self.current_token
    def parse(self):
        res = self.statements()
        if not res.error and self.current_token.type != T_EOF:
            return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end,"Token cannot appear after previous tokens"))
        return res

    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_token.pos_start.copy()
        while self.current_token.type == T_NEWLINE:
            res.register_move()
            self.move()
        statement = res.register(self.statement())
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
            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)
        return res.success(ListNode(statements,pos_start,self.current_token.pos_end.copy()))
    def statement(self):
        res = ParseResult()
        #pos_start = self.current_token.pos_start.copy()
        expr = res.register(self.expr())
        if res.error:
            return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end,"Expected 'if' int, float, identifier, '+', '-', '(', '[' or 'not'"))
        return res.success(expr)

    def call(self):
        res = ParseResult()
        atom = res.register(self.atom())
        if res.error: return res
        if self.current_token.type == T_PARENTIZQ:
            res.register_move()
            self.move()
            arg_nodes = []
            if self.current_token.type == T_PARENTDER:
                res.register_move()
                self.move()
            else:
                arg_nodes.append(res.register(self.expr()))
                if res.error:
                    return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end,"Expected ')','if', int, float, identifier, '+', '-', '(', '[' or 'not'"))
                while self.current_token.type == T_COMA:
                    res.register_move()
                    self.move()
                    arg_nodes.append(res.register(self.expr()))
                    if res.error: return res
                if self.current_token.type != T_PARENTDER:
                    return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end,f"Expected ',' or ')'"))
                res.register_move()
                self.move()
            return res.success(CallNode(atom, arg_nodes))
        return res.success(atom)
    def atom(self):
        res = ParseResult()
        token = self.current_token
        if token.type in (T_ENTERO, T_DECIMAL):
            res.register_move()
            self.move()
            return res.success(NumberNode(token))
        elif token.type == T_STRING:
            res.register_move()
            self.move()
            return res.success(StringNode(token))
        elif token.type == T_IDENTIFICADOR:
            res.register_move()
            self.move()
            return res.success(VarAccessNode(token))
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
        elif token.type == T_RECTIZQ:
            list_expr = res.register(self.list_expr())
            if res.error: return res
            return res.success(list_expr)
        elif token.matches(T_KEYWORD, 'if'):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)
        return res.failure(InvalidSyntaxError(token.pos_start, token.pos_end,"Expected int, float, identifier, '+', '-', '(', '[', 'if',"))
    def expr(self):
        res = ParseResult()
        if self.current_token.type == T_IDENTIFICADOR:
            variable_name = self.current_token
            res.register_move()
            self.move()
            if self.current_token.type == T_IGUAL:
                res.register_move()
                self.move()
                expr = res.register(self.expr())
                if res.error: return res
                return res.success(VarAssignNode(variable_name, expr))
            return res.success(VarAccessNode(variable_name))
        node = res.register(self.bin_operation(self.comp_expr, ((T_KEYWORD, "and"), (T_KEYWORD, 'or'))))
        if res.error:
            return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end,"Expected 'if', int, float, identifier, '+', '-' or '('"))
        return res.success(node)
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
            return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end,"Expected int, float, identifier, '+', '-', '(' or 'not', 'if'"))
        return res.success(node)
    def list_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_token.pos_start.copy()
        if self.current_token.type != T_RECTIZQ:
            return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end,f"Expected '['"))
        res.register_move()
        self.move()
        if self.current_token.type == T_RECTDER:
            res.register_move()
            self.move()
        else:
            element_nodes.append(res.register(self.expr()))
            if res.error:
                return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end,"Expected ']','if', int, float, identifier, '+', '-', '(', '[' or 'not'"))
            while self.current_token.type == T_COMA:
                res.register_move()
                self.move()
                element_nodes.append(res.register(self.expr()))
                if res.error: return res
            if self.current_token.type != T_RECTDER:
                return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end,f"Expected ',' or ']'"))
            res.register_move()
            self.move()
        return res.success(ListNode(element_nodes,pos_start,self.current_token.pos_end.copy()))
    def bin_operation(self, funcA, ops, funcB=None):
        if funcB == None : funcB = funcA
        res = ParseResult()
        left = res.register(funcA())
        if res.error: return res
        while self.current_token.type in ops or (self.current_token.type, self.current_token.value) in ops:
            op_token = self.current_token
            res.register_move()
            self.move()
            right = res.register(funcB())
            if res.error: return res
            left = BinOpNode(left, op_token, right)
        return res.success(left)
    def arith_expr(self):
        return self.bin_operation(self.term, (T_SUMA, T_MENOS))
    def term(self):
        return self.bin_operation(self.factor,(T_MULTIPLICA,T_DIVIDE))
    def power(self):
        return self.bin_operation(self.call, (T_POW,), self.factor)
    def factor(self):
        res = ParseResult()
        token = self.current_token
        if token.type in (T_SUMA, T_MENOS):
            res.register_move()
            self.move()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(token, factor))
        return self.power()

    def if_expr(self):
        res = ParseResult()
        all_cases = res.register(self.if_expr_cases('if'))
        if res.error: return res
        cases, else_case = all_cases
        return res.success(IfNode(cases, else_case))

    def if_expr_cases(self, case_keyword):
        res = ParseResult()
        cases = []
        else_case = None
        if not self.current_token.matches(T_KEYWORD, case_keyword):
            return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end,f"Expected '{case_keyword}'"))
        res.register_move()
        self.move()
        condition = res.register(self.expr())
        if res.error: return res

        if self.current_token.type != T_NEWLINE:
            return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end,f"Expected NEWLINE"))
        res.register_move()
        self.move()
        statements = res.register(self.statements())
        if res.error: return res
        cases.append((condition, statements, True))

        if not self.current_token.matches(T_KEYWORD, 'else'):
            return res.failure(InvalidSyntaxError(self.current_token.pos_start, self.current_token.pos_end,f"Expected 'else'"))
        res.register_move()
        self.move()
        return res.success((cases, else_case))
