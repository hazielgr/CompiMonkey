from interprete.RunTimeResult import RunTimeResult
from interprete.TablaDeSimbolos import TablaDeSimbolos
from interprete.Context import Context
from parsero.Parser import *
from lexico.Lexico import *
##########################################################
# Clase Interpreter: Definicion de funciones que visitan tipos de nodos
#########################################################
class Interpreter:
    def visit(self,node, context):
        method_name = f'visit_{type(node).__name__}'
        method=getattr(self,method_name,self.no_visit_method)
        return method(node,context)
    def no_visit_method(self,node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')
    def visit_NumberNode(self,node, context):
        return RunTimeResult().success( Numero(node.token.value).set_context(context).set_pos(node.pos_start,node.pos_end))
    def visit_StringNode(self, node, context):
        return RunTimeResult().success(String(node.token.value).set_context(context).set_pos(node.pos_start, node.pos_end))
    def visit_ListNode(self, node, context):
        res = RunTimeResult()
        elements = []
        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.error: return res
        return res.success(
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end))
    def visit_VarAccessNode(self, node, context):
        res = RunTimeResult()
        var_name = node.var_name_token.value
        value = context.symbol_table.get(var_name)
        if not value:
            return res.failure(RTError(node.pos_start, node.pos_end,f"'{var_name}' is not defined",context))
        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)
    def visit_VarAssignNode(self, node, context):
        res = RunTimeResult()
        var_name = node.var_name_token.value
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res
        context.symbol_table.set(var_name, value)
        return res.success(value)
    def visit_CallNode(self, node, context):
        res = RunTimeResult()
        args = []
        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.error: return res
        value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end)
        for arg_node in node.arg_nodes:
            args.append(res.register(self.visit(arg_node, context)))
            if res.error: return res
        return_value = res.register(value_to_call.execute(args))
        if res.error: return res
        return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(return_value)
    def visit_BinOpNode(self,node,context):
        res =  RunTimeResult()
        left= res.register(self.visit(node.left_node,context))
        if res.error: return res
        right= res.register(self.visit(node.right_node,context))
        if res.error:return res
        if node.op_token.type == T_SUMA:
            result, error = left.added_to(right)
        elif node.op_token.type == T_MENOS:
            result, error = left.subbed_by(right)
        elif node.op_token.type == T_MULTIPLICA:
            result, error = left.multiplied_by(right)
        elif node.op_token.type == T_DIVIDE:
            result, error = left.divided_by(right)
        elif node.op_token.type == T_POW:
            result, error = left.powed_by(right)
        elif node.op_token.type == T_COMP_IGUAL:
            result, error = left.get_comparison_equals(right)
        elif node.op_token.type == T_COMP_NO_IGUAL:
            result, error = left.get_comparison_notequals(right)
        elif node.op_token.type == T_COMP_MENORQUE:
            result, error = left.get_comparison_lowerthan(right)
        elif node.op_token.type == T_COMP_MAYORQUE:
            result, error = left.get_comparison_greaterthan(right)
        elif node.op_token.type == T_COMP_MENORIGUAL:
            result, error = left.get_comparison_lowerequal(right)
        elif node.op_token.type == T_COMP_MAYORIGUAL:
            result, error = left.get_comparison_greaterequal(right)
        elif node.op_token.matches(T_KEYWORD, 'and'):
            result, error = left.anded_by(right)
        elif node.op_token.matches(T_KEYWORD, 'or'):
            result, error = left.ored_by(right)
        if error:
            return  res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start,node.pos_end))
    def visit_UnaryOpNode(self,node, context):
        res = RunTimeResult()
        number = res.register(self.visit(node.node,context))
        if res.error: return res
        error =None
        if node.op_token.type == T_MENOS:
            number, error = number.multiplied_by(Numero(-1))
        elif node.op_token.matches(T_KEYWORD, 'not'):
            number, error = number.notted()
        if error: res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start,node.pos_end))
    def visit_IfNode(self, node, context):
        res = RunTimeResult()
        for condition, expr in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.error: return res
            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.error: return res
                return res.success(expr_value)
        if node.else_case:
            else_value = res.register(self.visit(node.else_case, context))
            if res.error: return res
            return res.success(else_value)
        return res.success(None)

    def visit_ForNode(self, node, context):
        res = RunTimeResult()
        elements = []
        start_value = res.register(self.visit(node.start_value_node, context))
        if res.error: return res
        end_value = res.register(self.visit(node.end_value_node, context))
        if res.error: return res
        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context))
            if res.error: return res
        else:
            step_value = Numero(1)
        i = start_value.value
        if step_value.value >= 0:
            condition = lambda: i < end_value.value
        else:
            condition = lambda: i > end_value.value
        while condition():
            context.symbol_table.set(node.var_name_token.value, Numero(i))
            i += step_value.value
            value = res.register(self.visit(node.body_node, context))
            if res.error: return res
            elements.append(value)
        return res.success(List(elements).set_context(context).set_pos(node.pos_start, node.pos_end))
    def visit_UntilNode(self, node, context):
        res = RunTimeResult()
        elements = []
        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.error: return res
            if not condition.is_true():
                break
            value = res.register(self.visit(node.body_node, context))
            if res.error:return res
            elements.append(value)
        return res.success(List(elements).set_context(context).set_pos(node.pos_start, node.pos_end))
    def visit_ReturnNode(self, node, context):
        res = RunTimeResult()
        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context))
            if res.error: return res
        return res.success(value)
    def visit_FuncDefNode(self, node, context):
        res = RunTimeResult()
        func_name = node.var_name_token.value if node.var_name_token else None
        body_node = node.body_node
        arg_names = [arg_name.value for arg_name in node.arg_name_tokens]
        func_value = Function(func_name, body_node, arg_names).set_context(context).set_pos(node.pos_start, node.pos_end)
        if node.var_name_token:
            context.symbol_table.set(func_name, func_value)
        return res.success(func_value)

##########################################################
# Clase Value: Posibles funciones que puede realizar Value
#########################################################
class Value:
    def __init__(self):
        self.set_pos()
        self.set_context()
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self
    def set_context(self, context=None):
        self.context = context
        return self
    def added_to(self, other):
        return None, self.illegal_operation(other)
    def subbed_by(self, other):
        return None, self.illegal_operation(other)
    def multiplied_by(self, other):
        return None, self.illegal_operation(other)
    def divided_by(self, other):
        return None, self.illegal_operation(other)
    def powed_by(self, other):
        return None, self.illegal_operation(other)
    def get_comparison_equals(self, other):
        return None, self.illegal_operation(other)
    def get_comparison_notequals(self, other):
        return None, self.illegal_operation(other)
    def get_comparison_lowerthan(self, other):
        return None, self.illegal_operation(other)
    def get_comparison_greaterthan(self, other):
        return None, self.illegal_operation(other)
    def get_comparison_lowerequal(self, other):
        return None, self.illegal_operation(other)
    def get_comparison_greaterequal(self, other):
        return None, self.illegal_operation(other)
    def anded_by(self, other):
        return None, self.illegal_operation(other)
    def ored_by(self, other):
        return None, self.illegal_operation(other)
    def notted(self,other):
        return None, self.illegal_operation(other)
    def execute(self, args):
        return RunTimeResult().failure(self.illegal_operation())
    def copy(self):
        raise Exception('No copy method defined')
    def is_true(self):
        return False
    def illegal_operation(self, other=None):
        if not other: other = self
        return RTError(self.pos_start, other.pos_end,'Illegal operation',self.context)
##########################################################
# Clase Numero: Posibles funciones que puede realizar numero
#########################################################
class Numero(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value
    def added_to(self,other):
        if isinstance(other,Numero):
            return Numero(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def subbed_by(self, other):
        if isinstance(other, Numero):
            return Numero(self.value - other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def multiplied_by(self, other):
        if isinstance(other, Numero):
            return Numero(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def divided_by(self, other):
        if isinstance(other, Numero):
            if other.value == 0:
                return None, RuntimeError(other.pos_start, other.pos_end, 'No es valida la division por cero', self.context)
            return Numero(self.value / other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def powed_by(self, other):
        if isinstance(other, Numero):
            return Numero(self.value ** other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def get_comparison_equals(self, other):
        if isinstance(other, Numero):
            return Numero(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def get_comparison_notequals(self, other):
        if isinstance(other, Numero):
            return Numero(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def get_comparison_lowerthan(self, other):
        if isinstance(other, Numero):
            return Numero(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def get_comparison_greaterthan(self, other):
        if isinstance(other, Numero):
            return Numero(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def get_comparison_lowerequal(self, other):
        if isinstance(other, Numero):
            return Numero(int(self.value <= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def get_comparison_greaterequal(self, other):
        if isinstance(other, Numero):
            return Numero(int(self.value >= other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def anded_by(self, other):
        if isinstance(other, Numero):
            return Numero(int(self.value and other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def ored_by(self, other):
        if isinstance(other, Numero):
            return Numero(int(self.value or other.value)).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def notted(self):
        return Numero(1 if self.value == 0 else 0).set_context(self.context), None
    def copy(self):
        copy = Numero(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    def is_true(self):
        return self.value != 0
    def __str__(self):
        return str(self.value)
    def __repr__(self):
        return str(self.value)

Numero.null = Numero(0)
Numero.false = Numero(0)
Numero.true = Numero(1)
##########################################################
# Clase String: Posibles funciones que puede realizar String
#########################################################
class String(Value):
    def __init__(self, value):
        super().__init__()
        self.value = value
    def added_to(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def multiplied_by(self, other):
        if isinstance(other, Numero):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, Value.illegal_operation(self, other)
    def is_true(self):
        return len(self.value) > 0
    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    def __str__(self):
        return self.value
    def __repr__(self):
        return f'"{self.value}"'
##########################################################
# Clase List: Posibles funciones que puede realizar List
#########################################################
class List(Value):
    def __init__(self, elements):
        super().__init__()
        self.elements = elements
    def added_to(self, other):
        new_list = self.copy()
        new_list.elements.append(other)
        return new_list, None
    def subbed_by(self, other):
        if isinstance(other, Numero):
            new_list = self.copy()
            try:
                new_list.elements.pop(other.value)
                return new_list, None
            except:
                return None, RTError(other.pos_start, other.pos_end,'Element at this index could not be removed from list because index is out of bounds',self.context)
        else:
            return None, Value.illegal_operation(self, other)
    def multiplied_by(self, other):
        if isinstance(other, List):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        else:
            return None, Value.illegal_operation(self, other)
    def divided_by(self, other):
        if isinstance(other, Numero):
            try:
                return self.elements[other.value], None
            except:
                return None, RTError(other.pos_start, other.pos_end,'Element at this index could not be retrieved from list because index is out of bounds',self.context)
        else:
            return None, Value.illegal_operation(self, other)
    def copy(self):
        copy = List(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    def __str__(self):
        return ", ".join([str(x) for x in self.elements])
    def __repr__(self):
        return f'[{", ".join([repr(x) for x in self.elements])}]'
class BaseFunction(Value):
    def __init__(self, name):
        super().__init__()
        self.name = name or "<NoNameFunc>"
    def generate_new_context(self):
        new_context = Context(self.name, self.context, self.pos_start)
        new_context.symbol_table = TablaDeSimbolos(new_context.parent.symbol_table)
        return new_context
    def check_args(self, arg_names, args):
        res = RunTimeResult()
        if len(args) > len(arg_names):
            return res.failure(RTError(self.pos_start, self.pos_end,f"{len(args) - len(arg_names)} too many args passed into {self}",self.context))
        if len(args) < len(arg_names):
            return res.failure(RTError(self.pos_start, self.pos_end,f"{len(arg_names) - len(args)} too few args passed into {self}",self.context))
        return res.success(None)
    def populate_args(self, arg_names, args, exec_ctx):
        for i in range(len(args)):
            arg_name = arg_names[i]
            arg_value = args[i]
            arg_value.set_context(exec_ctx)
            exec_ctx.symbol_table.set(arg_name, arg_value)
    def check_and_populate_args(self, arg_names, args, exec_ctx):
        res = RunTimeResult()
        res.register(self.check_args(arg_names, args))
        if res.error: return res
        self.populate_args(arg_names, args, exec_ctx)
        return res.success(None)
class Function(BaseFunction):
    def __init__(self, name, body_node, arg_names):
        super().__init__(name)
        self.body_node = body_node
        self.arg_names = arg_names
    def execute(self, args):
        res = RunTimeResult()
        interpreter = Interpreter()
        exec_ctx = self.generate_new_context()
        res.register(self.check_and_populate_args(self.arg_names, args, exec_ctx))
        if res.error: return res
        value = res.register(interpreter.visit(self.body_node, exec_ctx))
        if res.error: return res
        return res.success(value)
    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_names)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy
    def __repr__(self):
        return f"<function {self.name}>"

class CreateFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)
    def execute(self, args):
        res = RunTimeResult()
        exec_ctx = self.generate_new_context()
        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method)
        res.register(self.check_and_populate_args(method.arg_names, args, exec_ctx))
        if res.error: return res
        return_value = res.register(method(exec_ctx))
        if res.error: return res
        return res.success(return_value)

    def execute_print(self, exec_ctx):
        print(str(exec_ctx.symbol_table.get('value')))
        return RunTimeResult().success(Numero.null)
    execute_print.arg_names = ['value']

    def execute_say(self, exec_ctx):
        text = input()
        return RunTimeResult().success(String(text))
    execute_say.arg_names = []

    def execute_run(self, exec_ctx):
        fn = exec_ctx.symbol_table.get("fn")
        if not isinstance(fn, String):
            return RunTimeResult().failure(RTError(self.pos_start, self.pos_end,"Second argument must be string",exec_ctx))
        fn = fn.value
        try:
            with open(fn, "r") as f:
                script = f.read()
        except Exception as e:
            return RunTimeResult().failure(RTError(self.pos_start, self.pos_end,f"Failed to load script \"{fn}\"\n" + str(e),exec_ctx))
        error = run(fn, script)
        if error:
            return RunTimeResult().failure(RTError(self.pos_start, self.pos_end,f"Failed to finish executing script \"{fn}\"\n" +error.as_string(),exec_ctx))
        return RunTimeResult().success(Numero.null)
    execute_run.arg_names = ["fn"]

CreateFunction.run = CreateFunction("run")

tabla_simbolos_global = TablaDeSimbolos()
tabla_simbolos_global.set("null",Numero.null)
tabla_simbolos_global.set("no",Numero.false)
tabla_simbolos_global.set("si",Numero.true)
tabla_simbolos_global.set("RUN", CreateFunction.run)
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
