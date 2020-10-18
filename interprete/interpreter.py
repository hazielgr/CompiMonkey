from interprete.storage import *
from lexico.lexico import *
class Interpreter:
    def visit(self,node, context):
        method_name = f'visit_{type(node).__name__}'
        method=getattr(self,method_name,self.no_visit_method)
        return method(node,context)

    def no_visit_method(self,node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    #    print('Encontrado: Nodo_numero')
    def visit_NumberNode(self,node, context):
        return RunTimeResult().success( Numero(node.token.value).set_context(context).set_pos(node.pos_start,node.pos_end))

    #   print('Encontrado: Nodo_OperacioBinaria')
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
        if error:
            return  res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start,node.pos_end))

    #print('Encontrado: Nodo_OperacionUnaria')
    def visit_UnaryOpNode(self,node, context):
        res = RunTimeResult()
        number = res.register(self.visit(node.node,context))
        if res.error: return res

        error =  None

        if node.operation_token.type == T_RESTA:
            number, error = number.multiplied_by(Numero(-1))

        if error: res.failure(error)
        else:
            return res.success( number.set_pos(node.pos_start,node.pos_end))
