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