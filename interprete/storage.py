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
                return None, RuntimeError(other.pos_start, other.pos_end, 'No es valida la division por cero', self.context)
            return Numero(self.value / other.value).set_context(self.context), None

    def powed_by(self, other):
        if isinstance(other, Numero):
            return Numero(self.value ** other.value).set_context(self.context), None

    def get_comparison_equals(self, other):
        if isinstance(other, Numero):
            return Numero(int(self.value == other.value)).set_context(self.context), None

    def get_comparison_notequals(self, other):
        if isinstance(other, Numero):
            return Numero(int(self.value != other.value)).set_context(self.context), None

    def get_comparison_lowerthan(self, other):
        if isinstance(other, Numero):
            return Numero(int(self.value < other.value)).set_context(self.context), None

    def get_comparison_greaterthan(self, other):
        if isinstance(other, Numero):
            return Numero(int(self.value > other.value)).set_context(self.context), None

    def get_comparison_lowerequal(self, other):
        if isinstance(other, Numero):
            return Numero(int(self.value <= other.value)).set_context(self.context), None

    def get_comparison_greaterequal(self, other):
        if isinstance(other, Numero):
            return Numero(int(self.value >= other.value)).set_context(self.context), None

    def anded_by(self, other):
        if isinstance(other, Numero):
            return Numero(int(self.value and other.value)).set_context(self.context), None

    def ored_by(self, other):
        if isinstance(other, Numero):
            return Numero(int(self.value or other.value)).set_context(self.context), None

    def notted(self):
        return Number(1 if self.value == 0 else 0).set_context(self.context), None

    def copy(self):
        copy = Numero(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def __repr__(self):
        return str(self.value)