class ASTnode:
    def __init__(self, name, father):
        self.name = name
        self.father = father
        self.children = []
        self.type = None
        self.value = None

    def __str__(self):
        return "AST : [" +self.name+ " : [" +", ".join(self.children)+ "]]"

    def __repr__(self):
        return "AST : [" +self.name+ " : [" +", ".join(self.children)+ "]]"

    def set_father(self, father):
        self.father = father

    def set_children(self, children):
        self.children = children


class IF(ASTnode):
    def __init__(self, name, cond, cond_true, cond_false, father):
        ASTnode.__init__(self, name, father)
        self.children.append(cond)
        self.children.append(cond_true)
        self.children.append(cond_false)

    def __str__(self):
        return "IF : [" +self.name+ " : [" +", ".join(self.children)+ "]]"

    def __repr__(self):
        return "IF : [" +self.name+ " : [" +", ".join(self.children)+ "]]"


class Assing(ASTnode):
    def __init__(self, name, left, right, father):
        ASTnode.__init__(self, name)
        self.children.append(left)
        self.children.append(right)

    def __str__(self):
        return "Assign : [" +self.name+ " : [" +", ".join(self.children)+ "]]"

    def __repr__(self):
        return "Assign : [" +self.name+ " : [" +", ".join(self.children)+ "]]"