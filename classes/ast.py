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

    def set_type(self, type):
        self.type = type

    def print(self):
        if self.name in ['ASTnode', 'If', 'Attr', 'While', 'Expr']:
            print("<" + self.name + ">")
            for children in self.children:
                children.print()
            print("</" + self.name + ">")
        else:
            if self.name == 'Id' and not self.value in ['vint','vfloat']:
                parameters = " lexema=" + self.value + " type=" + self.type
            elif self.name == 'Num':
                parameters = " valor=" + self.value + " type=" + self.type
            else:
                parameters = " op=" + self.value
            print("<" + self.name + parameters + "/>")


