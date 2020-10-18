class Numero:
    def __init__(self,value):
        self.value = value
        self.set_pos()
        self.set_context()

    def set_context(self,context=None):
        self.context = context
        return self

    def set_pos(self,pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def added_to(self,other):
        if isinstance(other,Numero):
            return Numero(self.value + other.value).set_context(self.context), None

    def subbed_by(self, other):
        if isinstance(other, Numero):
            return Numero(self.value - other.value).set_context(self.context), None

    def multiplied_by(self, other):
        if isinstance(other, Numero):
            return Numero(self.value * other.value).set_context(self.context), None

    def divided_by(self, other):
        if isinstance(other, Numero):
            if other.value == 0:
                return None, RuntimeError(other.pos_start, other.pos_end, 'No es valida la division por cero'), self.context
            return Numero(self.value / other.value).set_context(self.context), None

    def __repr__(self):
        return str(self.value)