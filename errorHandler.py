from string_with_arrows import *
#################################
# MANEJAR ERRORES
#################################
class Error:

    # Maneja tipo de error, en donde esta leyendo
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

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, detalle=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', detalle)
