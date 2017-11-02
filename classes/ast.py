class ASTnode:
    def __init__(self, lexical, father=None):
        self.lexical = lexical
        self.father = father
        self.children = []
        self.type = None
        self.value = None

    def __str__(self):
        return "AST : [" +self.lexical+ " : [" +", ".join(self.children)+ "]]"

    def __repr__(self):
        return "AST : [" +self.lexical+ " : [" +", ".join(self.children)+ "]]"

    def set_father(self, father):
        self.father = father

    def set_children(self, children):
        self.children = children


class IF(ASTnode):
    def __init__(self, lexical, cond, father=None):
        ASTnode.__init__(self, lexical, father)
        self.children.append(cond)

    def __str__(self):
        return "IF : [" +self.lexical+ " : [" +", ".join(self.children)+ "]]"

    def __repr__(self):
        return "IF : [" +self.lexical+ " : [" +", ".join(self.children)+ "]]"


class While(ASTnode):
    def __init__(self, lexical, cond, father=None):
        ASTnode.__init__(self, lexical, father)
        self.children.append(cond)

    def __str__(self):
        return "While : [" +self.lexical+ " : [" +", ".join(self.children)+ "]]"

    def __repr__(self):
        return "While : [" +self.lexical+ " : [" +", ".join(self.children)+ "]]"


class Attr(ASTnode):
    def __init__(self, lexical, left, right, father=None):
        ASTnode.__init__(self, lexical)
        self.children.append(left)
        self.children.append(right)

    def __str__(self):
        return "Attr : [" +self.lexical+ " : [" +", ".join(self.children)+ "]]"

    def __repr__(self):
        return "Attr : [" +self.lexical+ " : [" +", ".join(self.children)+ "]]"


class ID(ASTnode):
    def __init__(self, lexical, token_type, father=None):
        ASTnode.__init__(self, lexical)
        self.type = token_type

    def __str__(self):
        return "ID : [" +self.lexical+ " : [" +", ".join(self.children)+ "]]"

    def __repr__(self):
        return "ID : [" +self.lexical+ " : [" +", ".join(self.children)+ "]]"


class Num(ASTnode):
    def __init__(self, lexical, father=None):
        ASTnode.__init__(self, lexical)

    def __str__(self):
        return "Num : [" +self.lexical+ " : [" +", ".join(self.children)+ "]]"

    def __repr__(self):
        return "Num : [" +self.lexical+ " : [" +", ".join(self.children)+ "]]"


class Read(ASTnode):
    def __init__(self, lexical, children, father=None):
        ASTnode.__init__(self, lexical)
        self.children.append(children)

    def __str__(self):
        return "Read : [" +self.lexical+ " : [" +", ".join(self.children)+ "]]"

    def __repr__(self):
        return "Read : [" +self.lexical+ " : [" +", ".join(self.children)+ "]]"


class Print(ASTnode):
    def __init__(self, lexical, children, father=None):
        ASTnode.__init__(self, lexical)
        self.children.append(children)

    def __str__(self):
        return "Print : [" +self.lexical+ " : [" +", ".join(self.children)+ "]]"

    def __repr__(self):
        return "Print : [" +self.lexical+ " : [" +", ".join(self.children)+ "]]"


class LogicalOp(ASTnode):
    def __init__(self, lexical, left, right, father=None):
        ASTnode.__init__(self, lexical)
        self.children.append(left)
        self.children.append(right)

    def __str__(self):
        return "LogicalOp : [" +self.lexical+ " : [" +", ".join(self.children)+ "]]"

    def __repr__(self):
        return "Num : [" +self.lexical+ " : [" +", ".join(self.children)+ "]]"


class RelOp(ASTnode):
    def __init__(self, lexical, left, right, father=None):
        ASTnode.__init__(self, lexical)
        self.children.append(left)
        self.children.append(right)

    def __str__(self):
        return "RelOp : [" +self.lexical+ " : [" +", ".join(self.children)+ "]]"

    def __repr__(self):
        return "RelOp : [" +self.lexical+ " : [" +", ".join(self.children)+ "]]"


class ArithOp(ASTnode):
    def __init__(self, lexical, left, right, father=None):
        ASTnode.__init__(self, lexical)
        self.children.append(left)
        self.children.append(right)

    def __str__(self):
        return "ArithOp : [" +self.lexical+ " : [" +", ".join(self.children)+ "]]"

    def __repr__(self):
        return "ArithOp : [" +self.lexical+ " : [" +", ".join(self.children)+ "]]"