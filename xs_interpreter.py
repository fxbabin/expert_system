class Interpreter(object):

    def __init__(self):
        pass
        
    def interpret(self, node, graph):
        if node:
            if type(node).__name__ == "Node_condition":
                return abs(self.apply_logical(node, node.left, node.right, graph) - node.neg)
            if type(node).__name__ == "Node_letter":
                implies_node = graph.find_letter_in_implies(node.name)
                if implies_node:
                    for child in implies_node.childs_pos:
                        if self.interpret(child, graph) == 1:
                            node.state = 1
                    for child in implies_node.childs_neg:
                        if self.interpret(child, graph) == 1:
                            node.state = 0
                return abs(node.state - node.neg)
    
    def apply_logical(self, node, left, right, graph):
        if node.token.type == "AND":
            return self.interpret(left, graph) & self.interpret(right, graph)
        if node.token.type == "OR":
            return self.interpret(left, graph) | self.interpret(right, graph)
        if node.token.type == "XOR":
            return self.interpret(left, graph) ^ self.interpret(right, graph)
