from classes.three_addr import *


class ASTNode:
    def __init__(self, lexical, father=None):
        self.lexical = lexical
        self.father = father
        self.children = []
        self.type = None
        self.value = None
        self.true_label = None
        self.false_label = None

    def __str__(self):
        return "AST : [" + self.lexical + " : [" + ", ".join(self.children) + "]]"

    def __repr__(self):
        return "AST : [" + self.lexical + " : [" + ", ".join(self.children) + "]]"

    def set_father(self, father):
        self.father = father

    def set_children(self, children):
        self.children.append(children)

    def generate_code(self, out):
        for children in self.children:
            children.generate_code(out)


class IF(ASTNode):
    def __init__(self, lexical, cond, father=None):
        ASTNode.__init__(self, lexical, father)
        self.children.append(cond)
        self.next = None

    def __str__(self):
        return "IF : [" + self.lexical + " : [" + ", ".join(self.children) + "]]"

    def __repr__(self):
        return "IF : [" + self.lexical + " : [" + ", ".join(self.children) + "]]"

    def generate_code(self, out):
        self.next = Label()
        if len(self.children) == 3:
            self.children[0].true_label = Label()
            self.children[0].false_label = Label()
            self.children[0].next = self.children[1].next = self.next
            self.children[0].generate_branch_code(out)
            if self.children[0].addr:
                out.write("if " + self.children[0].addr.name + " == 0 goto " +
                          self.children[0].false_label.name + "\n"
                          )
            else:
                out.write(self.children[0].true_label.name + ": ")
            self.children[1].generate_code(out)
            out.write("goto " + self.next.name + "\n")
            out.write(self.children[0].false_label.name + ": ")
            self.children[2].generate_code(out)
        else:
            self.children[0].true_label = Label()
            self.children[0].false_label = self.children[1].next = self.next
            self.children[0].generate_branch_code(out)
            if self.children[0].addr:
                out.write("if " + self.children[0].addr.name + " == 0 goto " + self.children[0] + \
                          self.children[0].false_label.name + "\n"
                          )
            else:
                out.write(self.children[0].true_label.name + ": ")
            self.children[1].generate_code(out)
        out.write(self.next.name + ": ")


class While(ASTNode):
    def __init__(self, lexical, cond, father=None):
        ASTNode.__init__(self, lexical, father)
        self.children.append(cond)
        self.next = None
        self.begin = None

    def __str__(self):
        return "While : [" + self.lexical + " : [" + ", ".join(self.children) + "]]"

    def __repr__(self):
        return "While : [" + self.lexical + " : [" + ", ".join(self.children) + "]]"

    def generate_code(self, out):
        self.begin = Label()
        self.children[0].true_label = Label()
        self.children[0].false_label = self.next = Label()
        self.children[1].next = self.begin
        out.write(self.begin.name + ": ")
        self.children[0].generate_branch_code(out)
        if self.children[0].addr:
            out.write("if " + self.children[0].addr.name + " == 0 goto " +
                      self.children[0].false_label.name + "\n"
                      )
        else:
            out.write(self.children[0].true_label.name + ": ")
        self.children[1].generate_code(out)
        out.write("goto " + self.begin.name + "\n")
        out.write(self.next.name + ": ")


class Attr(ASTNode):
    def __init__(self, lexical, left, right, father=None):
        ASTNode.__init__(self, lexical)
        self.children.append(left)
        self.children.append(right)

    def __str__(self):
        return "Attr : [" + self.lexical + " : [" + ", ".join(self.children) + "]]"

    def __repr__(self):
        return "Attr : [" + self.lexical + " : [" + ", ".join(self.children) + "]]"

    def generate_code(self, out):
        self.children[0].generate_code(out)
        self.children[1].generate_r_value_code(out)
        self.children[0].addr.temp = self.children[1].addr.temp
        out.write(self.children[0].addr.name + " = " + self.children[1].addr.name + "\n")


class ID(ASTNode):
    def __init__(self, lexical, token_type, father=None):
        ASTNode.__init__(self, lexical)
        self.type = token_type
        self.operand = None
        self.addr = None

    def __str__(self):
        return "ID : [" + self.lexical + " : [" + ", ".join(self.children) + "]]"

    def __repr__(self):
        return "ID : [" + self.lexical + " : [" + ", ".join(self.children) + "]]"

    def generate_code(self, out):
        self.operand = Operand()
        self.operand.tableEntry = self.lexical
        self.operand.name = self.lexical
        self.addr = self.operand

    def generate_r_value_code(self, out):
        self.generate_code(out)

    def generate_branch_code(self, out):
        self.generate_code(out)


class Num(ASTNode):
    def __init__(self, lexical, token_type, token_value, father=None):
        ASTNode.__init__(self, lexical)
        self.type = token_type
        self.value = token_value
        self.operand = None
        self.addr = None

    def __str__(self):
        return "Num : [" + self.lexical + " : [" + ", ".join(self.children) + "]]"

    def __repr__(self):
        return "Num : [" + self.lexical + " : [" + ", ".join(self.children) + "]]"

    def generate_code(self, out):
        self.operand = Operand()
        self.operand.name = self.lexical
        self.addr = self.operand

    def generate_r_value_code(self, out):
        self.generate_code(out)

    def generate_branch_code(self, out):
        self.generate_code(out)


class Read(ASTNode):
    def __init__(self, lexical, children, father=None):
        ASTNode.__init__(self, lexical)
        self.children.append(children)

    def __str__(self):
        return "Read : [" + self.lexical + " : [" + ", ".join(self.children) + "]]"

    def __repr__(self):
        return "Read : [" + self.lexical + " : [" + ", ".join(self.children) + "]]"


class Print(ASTNode):
    def __init__(self, lexical, children, father=None):
        ASTNode.__init__(self, lexical)
        self.children.append(children)

    def __str__(self):
        return "Print : [" + self.lexical + " : [" + ", ".join(self.children) + "]]"

    def __repr__(self):
        return "Print : [" + self.lexical + " : [" + ", ".join(self.children) + "]]"


class LogicalOp(ASTNode):
    def __init__(self, lexical, left, right, father=None):
        ASTNode.__init__(self, lexical)
        self.children.append(left)
        self.children.append(right)
        self.addr = None

    def __str__(self):
        return "LogicalOp : [" + self.lexical + " : [" + ", ".join(self.children) + "]]"

    def __repr__(self):
        return "Num : [" + self.lexical + " : [" + ", ".join(self.children) + "]]"

    def generate_branch_code(self, out):
        if self.lexical == "||":
            self.children[0].true_label = self.true_label
            self.children[0].false_label = Label()
            self.children[1].true_label = self.true_label
            self.children[1].false_label = self.false_label
            self.children[0].generate_branch_code(out)
            if self.children[0].addr:
                out.write("if " + self.children[0].addr.name + " != 0 goto " +
                          self.children[0].true_label.name + "\n"
                          )
            else:
                out.write(self.children[0].false_label.name + ": ")
            self.children[1].generate_branch_code(out)
            if self.children[1].addr:
                out.write("if " + self.children[1].addr.name + " == 0 goto " +
                          self.children[1].false_label.name + "\n"
                          )
                out.write("goto " + self.children[1].true_label.name + "\n")
        elif self.lexical == "&&":
            self.children[0].true_label = Label()
            self.children[0].false_label = self.false_label
            self.children[1].true_label = self.true_label
            self.children[1].false_label = self.false_label
            self.children[0].generate_branch_code(out)
            if self.children[0].addr:
                out.write("if " + self.children[0].addr.name + " == 0 goto " +
                          self.children[0].false_label.name + "\n"
                          )
            else:
                out.write(self.children[0].true_label.name + ": ")
            self.children[1].generate_branch_code(out)
            if self.children[1].addr:
                out.write("if " + self.children[1].addr.name + " == 0 goto " +
                          self.children[1].false_label.name + "\n"
                          )
                out.write("goto " + self.children[1].true_label.name + "\n")


class RelOp(ASTNode):
    def __init__(self, lexical, left, right, father=None):
        ASTNode.__init__(self, lexical)
        self.children.append(left)
        self.children.append(right)
        self.addr = None

    def __str__(self):
        return "RelOp : [" + self.lexical + " : [" + ", ".join(self.children) + "]]"

    def __repr__(self):
        return "RelOp : [" + self.lexical + " : [" + ", ".join(self.children) + "]]"

    def generate_branch_code(self, out):
        self.children[0].generate_branch_code(out)
        self.children[1].generate_branch_code(out)
        test = self.children[0].addr.name + " " + self.lexical + " " + \
               self.children[1].addr.name
        out.write("if " + test + " goto " + self.true_label.name + "\n")
        out.write("goto " + self.false_label.name + "\n")

    def generate_r_value_code(self, out):
        self.children[0].generate_branch_code(out)
        self.children[1].generate_branch_code(out)
        test = self.children[0].addr.name + " " + self.lexical + " " + \
               self.children[1].addr.name
        temp = Temp()
        self.true_label = Label()
        self.false_label = Label()
        self.next = Label()
        self.addr = Operand()
        self.addr.temp = temp
        self.addr.name = temp.name
        out.write("if " + test + " goto " + self.true_label.name + "\n")
        out.write("goto " + self.false_label.name + "\n")
        out.write(self.true_label.name + ": " + temp.name + " = 1\n")
        out.write("goto " + self.next.name + "\n")
        out.write(self.false_label.name + ": " + temp.name + " = 0\n")
        out.write(self.next.name + ": ")


class ArithOp(ASTNode):
    def __init__(self, lexical, left, right, father=None):
        ASTNode.__init__(self, lexical)
        self.children.append(left)
        self.children.append(right)

    def __str__(self):
        return "ArithOp : [" + self.lexical + " : [" + ", ".join(self.children) + "]]"

    def __repr__(self):
        return "ArithOp : [" + self.lexical + " : [" + ", ".join(self.children) + "]]"

    def generate_branch_code(self, out):
        self.children[0].generate_branch_code(out)
        self.children[1].generate_branch_code(out)
        temp = Temp()
        self.addr = Operand()
        self.addr.temp = temp
        self.addr.name = temp.name
        out.write(temp.name + " = " + self.children[0].addr.name + " " + self.lexical +
                  " " + self.children[1].addr.name + "\n"
                 )

    def generate_r_value_code(self, out):
        self.children[0].generate_r_value_code(out)
        self.children[1].generate_r_value_code(out)
        temp = Temp()
        self.addr = Operand()
        self.addr.temp = temp
        self.addr.name = temp.name
        out.write(temp.name + " = " + self.children[0].addr.name + " " + self.lexical +
                  " " + self.children[1].addr.name + "\n"
                 )
