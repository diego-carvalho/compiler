class Operand:
    def __init__(self):
        self.name = None
        self.temp = None
        self.tableEntry = None
        self.type = None


class Temp:
    temp_number = 0

    def __init__(self):
        self.n = None
        self.name = "t" + str(Temp.temp_number)
        Temp.temp_number += 1


class Label(Operand):
    label_number = 0

    def __init__(self):
        Operand.__init__(self)
        self.n = None
        self.name = "L" + str(Label.label_number)
        Label.label_number += 1


class Tac:
    def __init__(self, format, src1, src2, dst=None, dst_goto=None):
        self.name = None
        self.format = format
        self.dst = dst
        self.dst_goto = dst_goto
        self.src1 = src1
        self.src2 = src2