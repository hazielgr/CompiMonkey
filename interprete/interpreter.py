from interprete.InterpFunc import *
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
    def visit_varAccessNode(self, node, context):
        res = RunTimeResult()
        var_name = node.var_name_token.value
        value = context.symbol_table.get(var_name)
        if not value:
            return res.failure(RTError(node.pos_start, node.pos_end,f"'{var_name}' is not defined",context))
        value = value.copy().set_pos(node.pos_start, node.pos_end)
        return res.success(value)
    def visit_varAssignNode(self, node, context):
        res = RunTimeResult()
        var_name = node.var_name_token.value
        value = res.register(self.visit(node.value_node, context))
        if res.error: return res
        context.symbol_table.set(var_name, value)
        return res.success(value)
    def visit_ListNode(self, node, context):
        res = RunTimeResult()
        elements = []
        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.error: return res
        return res.success(
            List(elements).set_context(context).set_pos(node.pos_start, node.pos_end))
    def visit_BinOpNode(self,node,context):
        res =  RunTimeResult()
        left= res.register(self.visit(node.left_node,context))
        if res.error: return res
        right= res.register(self.visit(node.right_node,context))
        if res.error:return res
        if node.op_token.type == T_SUMA:
            result, error = left.added_to(right)
        elif node.op_token.type == T_RESTA:
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
        if node.operation_token.type == T_RESTA:
            number, error = number.multiplied_by(Numero(-1))
        elif node.op_token.matches(T_KEYWORD, 'not'):
            number, error = number.notted()
        if error: res.failure(error)
        else:
            return res.success(number.set_pos(node.pos_start,node.pos_end))