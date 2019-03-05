from es_node import Node_letter, Node_condition
from es_token import Token

class Interpreter(object):
    
    def __init__(self):
        pass
        
    def interpret(self, node):
        if node:
            if type(node).__name__ == "Node_condition":
                return abs(self.apply_logical(node, node.left, node.right) - node.neg)
            if type(node).__name__ == "Node_letter":
                for child in (node.childs_pos + node.childs_neg):
                    if self.interpret(child) == 1:
                        node.state = 1
                return abs(node.state - node.neg)
    
    def apply_logical(self, node, left, right):
        if node.token.type == "AND":
            return self.interpret(left) & self.interpret(right)
        if node.token.type == "OR":
            return self.interpret(left) | self.interpret(right)
        if node.token.type == "XOR":
            return self.interpret(left) ^ self.interpret(right)
                

