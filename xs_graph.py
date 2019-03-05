from xs_interpreter import Interpreter


class Graph(object):

    def __init__(self):
        self.implies_list = []
        self.implies_name_list = []
        self.true_facts = ""
        self.interpretor = Interpreter()

    def error(self, s):
        raise Exception(s)

    def add_new_AST(self, root):
        self.update_implies_list(root.right)
        self.update_graph(root.left, root.right)

    def update_implies_list(self, node):
        if node:
            if type(node).__name__ == "Node_letter":
                if node.name not in self.implies_name_list:
                    self.implies_list.append(node)
                    self.implies_name_list.append(node.name)
            if type(node).__name__ == "Node_condition":
                self.update_implies_list(node.left)
                self.update_implies_list(node.right)

    def update_graph(self, left, node):
        if node:
            if type(node).__name__ == "Node_letter":
                if node.neg == 1:
                    (self.find_letter_in_implies(node.name)
                        .childs_neg.append(left))
                else:
                    (self.find_letter_in_implies(node.name)
                        .childs_pos.append(left))
            if type(node).__name__ == "Node_condition":
                self.update_graph(left, node.left)
                self.update_graph(left, node.right)

    def find_letter_in_implies(self, name):
        for node in self.implies_list:
            if node.name == name:
                return node
        return None

    def learn_facts(self, true_facts):
        self.true_facts = true_facts

    def set_facts(self, node):
        if node:
            if type(node).__name__ == "Node_letter":
                for child in (node.childs_pos + node.childs_neg):
                    self.set_facts(child)
                if node.token.value in self.true_facts:
                    node.state = 1
            if type(node).__name__ == "Node_condition":
                self.set_facts(node.left)
                self.set_facts(node.right)

    def query(self, letter):
        if letter in self.full_history.keys():
            print("{} is {}".format(letter, self.full_history[letter]))
            return self.full_history[letter]
        elif letter in self.true_facts:
            print("{} is True".format(letter))
            return True
        else:
            print("{} is False".format(letter))
            return False

    def check_contradiction(self):
        self.full_history = {}
        for node in self.implies_list:
            self.full_history[node.name] = self.get_final_state(node)
            if self.full_history[node.name] is None:
                if node.name in self.true_facts:
                    self.full_history[node.name] = True
                else:
                    self.full_history[node.name] = False

    def get_final_state(self, node):
        history = []
        for child in node.childs_pos:
            res = self.interpretor.interpret(child, self)
            if res == 1:
                history.append(True)

        for child in node.childs_neg:
            res = self.interpretor.interpret(child, self)
            if res == 1:
                history.append(False)

        if len(set(history)) == 0:
            return
        elif len(set(history)) == 1:
            return history[0]
        else:
            self.error("Error contradiction found with letter {}"
                       .format(node.name))
