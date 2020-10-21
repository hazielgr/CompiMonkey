from errores.string_with_arrows import *
##########################################################
# Clase Error: Manejo de posibles erroes del interprete
#########################################################
class Error:
    def __init__(self,pos_start,pos_end, error_name, detalle):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.detalle = detalle

    def as_string(self):
        result = f'{self.error_name}: {self.detalle}\n'
        result += f'File{self.pos_start.fn}, line {self.pos_start.ln +1}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result

class IllegalCharacError(Error):
    def __init__(self,pos_start,pos_end,detalle):
        super().__init__(pos_start,pos_end,'Illegal Character',detalle)

class ExpectedCharacError(Error):
    def __init__(self, pos_start, pos_end, detalle):
        super().__init__(pos_start, pos_end, 'Expected Character', detalle)

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, detalle=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', detalle)

class RTError(Error):
    def __init__(self, pos_start, pos_end, detalle, context):
        super().__init__(pos_start, pos_end, 'Runtime Error', detalle)
        self.context = context

    def as_string(self):
        result  = self.generate_traceback()
        result += f'{self.error_name}: {self.detalle}'
        result += '\n\n' + string_with_arrows(self.pos_start.ftxt, self.pos_start, self.pos_end)
        return result
    def generate_traceback(self):
        result = ''
        pos = self.pos_start
        ctx = self.context
        while ctx:
            result = f'  File {pos.fn}, line {str(pos.ln + 1)}, in {ctx.display_name}\n' + result
            pos = ctx.parent_entry_pos
            ctx = ctx.parent
        return 'Traceback (most recent call last):\n' + result
