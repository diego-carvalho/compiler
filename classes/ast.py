class ASTnode:
    def __init__(self, name):
        self.children = []
        self.name = name
        self.value = ""
        self.type = ""
        print("Nó criado: " + self.name)

    def addChildren(self, node):
        self.children.append(node)

    def set_value(self, value):
        self.value = value
        if self.value == '<=':
            self.value == 'leq'

    def set_type(self, type):
        self.type = type

    def print(self):
        if self.name in ['ASTnode', 'If', 'Attr', 'While', 'Expr']:
            print("<" + self.name + ">")
            for children in self.children:
                children.print()
            print("</" + self.name + ">")
        elif self.name in ['ArithOp', 'LogicalOp']:
            print("<" + self.name + " op='" + self.value + "'>")
            for children in self.children:
                children.print()
            print("</" + self.name + ">")
        else:
            parameters = ""
            if self.name == 'Id':
                parameters = " lexema='" + self.value + "' type='" + self.type + "'"
            elif self.name == 'Num':
                parameters = " valor='" + self.value + "' type='" + self.type + "'"
            print("<" + self.name + parameters + "/>")


