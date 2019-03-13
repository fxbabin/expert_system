class Interpreter(object):

    def __init__(self):
        self.graph_list = {}
        self.all_histories = []
        pass

    def interpret(self, node, graph):
        if node:
            if type(node).__name__ == "Node_condition":
                return self.apply_logical(node, node.left, node.right, graph)
            node.visited = 1 
            if type(node).__name__ == "Node_letter":
                implies_node = graph.find_letter_in_implies(node.name)
                if implies_node:
                    for child in implies_node.childs_pos:
                        if child.visited == 0:
                            if self.interpret(child, graph) == 1:
                                node.state = 1 
                    for child in implies_node.childs_neg:
                        if child.visited == 0:
                            if self.interpret(child, graph) == 1:
                                node.state = 0 
                node.visited = 0 
                return abs(node.state - node.neg)
            

    def apply_logical(self, node, left, right, graph):
        if node.token.type == "AND":
            return abs((self.interpret(left, graph) & self.interpret(right, graph)) - node.neg)
        if node.token.type == "OR":
            return abs((self.interpret(left, graph) | self.interpret(right, graph)) - node.neg)
        if node.token.type == "XOR":
            return abs((self.interpret(left, graph) ^ self.interpret(right, graph)) - node.neg)
