from xs_interpreter import Interpreter
import copy

class Graph(object):

    def __init__(self):
        self.ast_list = []
        self.implies_list = []
        self.implies_name_list = []
        self.true_facts = ""
        self.incoherent = 0
        self.interpretor = Interpreter()
        self.full_history = {}
        self.list_copy = []
        self.list_copy_rule = []
        self.display_tables = False

    def error(self, s):
        raise Exception(s)

    def add_new_AST(self, root):
        self.update_implies_list(root.right)
        self.update_graph(root.left, root.right, 0)
        self.ast_list.append(root.right)
        if root.token.type == "ONLY_IF":
            self.update_implies_list(root.left)
            self.update_graph(root.right, root.left, 0)
            self.ast_list.append(root.left)

    def update_implies_list(self, node):
        if node:
            if type(node).__name__ == "Node_letter":
                if node.name not in self.implies_name_list:
                    self.implies_list.append(node)
                    self.implies_name_list.append(node.name)
            if type(node).__name__ == "Node_condition":
                self.update_implies_list(node.left)
                self.update_implies_list(node.right)

    def update_graph(self, left, node, neg):
        if node:
            if type(node).__name__ == "Node_letter":
                if abs(node.neg - neg) == 1:
                    (self.find_letter_in_implies(node.name)
                        .childs_neg.append(left))
                else:
                    (self.find_letter_in_implies(node.name)
                        .childs_pos.append(left))
            if type(node).__name__ == "Node_condition":
                if node.token.type == "OR" or node.token.type == "XOR":
                    self.update_ind_dics(left, node)
                    self.incoherent += 1
                self.update_graph(left, node.left, abs(node.neg - neg))
                self.update_graph(left, node.right, abs(node.neg - neg))

    def update_ind_dics(self, left, node):
        if node.token.type == "OR":
            if type(node.left).__name__ == "Node_letter":
                self.find_letter_in_implies(node.left.name).or_dic[left] = node.right
            else:
                node.left.or_dic[left] = node.right
            if type(node.right).__name__ == "Node_letter":
                self.find_letter_in_implies(node.right.name).or_dic[left] = node.left
            else:
                node.right.or_dic[left] = node.left
        if node.token.type == "XOR":
            if type(node.left).__name__ == "Node_letter":
                self.find_letter_in_implies(node.left.name).xor_dic[left] = node.right
            else:
                node.left.xor_dic[left] = node.right
            if type(node.right).__name__ == "Node_letter":
                self.find_letter_in_implies(node.right.name).xor_dic[left] = node.left
            else:
                node.right.xor_dic[left] = node.left
            
    def find_letter_in_implies(self, name):
        for node in self.implies_list:
            if node.name == name:
                return node
        return None

    def learn_facts(self, true_facts):
        self.true_facts = true_facts

    def set_facts(self, node):
        if node:
            node.visited = 1
            if type(node).__name__ == "Node_letter":
                for child in (node.childs_pos + node.childs_neg):
                    if child.visited == 0:
                        self.set_facts(child)
                if node.token.value in self.true_facts:
                    node.state = 1 
            if type(node).__name__ == "Node_condition":
                self.set_facts(node.left)
                self.set_facts(node.right)
            node.visited = 0
        
    def query(self, letter):
        if letter in self.full_history.keys():
            if self.full_history[letter] != None:
                print("{} is {}".format(letter, self.full_history[letter]))
                return self.full_history[letter]
        if letter in self.true_facts:
            print("{} is True".format(letter))
            return True
        else:
            print("{} is False".format(letter))
            return False

    def resolve_simple(self):
        for node in self.implies_list:
            self.full_history[node.name] = self.get_simple_final_state(node)
            if self.full_history[node.name] is None:
                if node.name in self.true_facts:
                    self.full_history[node.name] = True
                else:
                    self.full_history[node.name] = False
        return self.full_history
    
    def get_simple_final_state(self, node):
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
   
    def merge_new_graph(self, new):
        if self.tmp_history == {}:
            self.tmp_history = new
            return
        for letter, state in new.items():
            if state != self.tmp_history[letter]:
                self.tmp_history[letter] = "IND"
                
    def resolve_complex(self):
        self.check_ind_rules(self, self, None, 0)
        self.tmp_history = {}
        for copy_graph in self.list_copy:
            hist = copy_graph.resolve_simple()
            self.merge_new_graph(hist)
        self.full_history = self.tmp_history
        if self.display_tables:
            self.display_table()
    
    def handle_xor(self, origin_graph, current_graph, prev_rule, prev_case, node, rule, mirror):
        if prev_case == 1 or prev_case == 2 or prev_case == 6 or prev_case == 7:
            self.add_recursively_rule(node, prev_rule)
            self.add_recursively_rule(mirror, prev_rule)
        
        for index in range(0, len(current_graph.list_copy_rule)):
            if node in current_graph.list_copy_rule[index]:
                self.add_recursively_rule(node, current_graph.list_copy_rule[index][0])
                self.add_recursively_rule(mirror, current_graph.list_copy_rule[index][0])
                del current_graph.list_copy_rule[index]
                prev_case = 4
                break
                
        copy_graph_1 = copy.deepcopy(current_graph)
        copy_graph_2 = copy.deepcopy(current_graph)
        copy_rule = None
        case = 0
        if type(mirror).__name__ == "Node_condition" and type(node).__name__ == "Node_condition":
            case = 3
            if prev_case == 0 or prev_case == 3:
                copy_rule_1, copy_node_1 = self.set_special_xor(rule, node, current_graph, copy_graph_1, 1)
                copy_rule_2, copy_node_2 = self.set_special_xor(rule, node, current_graph, copy_graph_2, 2)                
                self.check_ind_rules(origin_graph, copy_graph_1, copy_rule_1, 3)
                self.check_ind_rules(origin_graph, copy_graph_2, copy_rule_2, 3)
            elif prev_case == 1 or prev_case == 2 or prev_case == 4 or prev_case == 5:
                copy_rule_1 = self.set_special_xor(rule, node, current_graph, copy_graph_1, 3)
                copy_rule_2 = self.set_special_xor(rule, node, current_graph, copy_graph_2, 4)
                self.check_ind_rules(origin_graph, copy_graph_1, copy_rule_1, 3)
                self.check_ind_rules(origin_graph, copy_graph_2, copy_rule_2, 3)                
                
        if type(mirror).__name__ == "Node_condition" and case != 3:
            copy_node = copy_graph_1.find_letter_in_implies(node.name)
            copy_rule = self.get_copy_rule(node, rule, copy_node, copy_graph_1)
            self.handle_neg(copy_rule, copy_node, 0)
            self.handle_neg(copy_rule, copy_node.xor_dic[copy_rule[0]], 1)
            if mirror.neg == 1:
                case = 6
            else:
                case = 1
            
        if type(node).__name__ == "Node_condition" and case != 3:
            copy_node = copy_graph_1.find_letter_in_implies(mirror.name)
            copy_rule = self.get_copy_rule(mirror, rule, copy_node, copy_graph_1)
            self.handle_neg(copy_rule, copy_node, 0)
            self.handle_neg(copy_rule, copy_node.xor_dic[copy_rule[0]], 1)
            if node.neg == 1:
                case = 7
            else:
                case = 2
        
        if prev_case == 0:
            if case == 0 or case == 1 or case == 6:
                self.set_rules_xor(rule, node, copy_graph_1, 1)
                self.set_rules_xor(rule, node, copy_graph_2, 2)
            elif case == 2 or case == 7:
                self.set_rules_xor(rule, mirror, copy_graph_1, 1)
                self.set_rules_xor(rule, mirror, copy_graph_2, 2)
        if prev_case == 1:
            if case == 0 or case == 1 or case == 6:
                self.set_rules_xor(rule, node, copy_graph_1, 3)
                self.set_rules_xor(rule, node, copy_graph_2, 4)
            elif case == 2 or case == 7:
                self.set_rules_xor(rule, mirror, copy_graph_1, 3)
                self.set_rules_xor(rule, mirror, copy_graph_2, 4)
        if prev_case == 2:
            if case == 0 or case == 1 or case == 6:
                self.set_rules_xor(rule, node, copy_graph_1, 3)
                self.set_rules_xor(rule, node, copy_graph_2, 4)
            elif case == 2 or case == 7:
                self.set_rules_xor(rule, mirror, copy_graph_1, 3)
                self.set_rules_xor(rule, mirror, copy_graph_2, 4)
        if prev_case == 3:
            if case == 0 or case == 1 or case == 6:
                self.set_rules_xor(rule, node, copy_graph_1, 1)
                self.set_rules_xor(rule, node, copy_graph_2, 2)
            elif case == 2 or case == 7:
                self.set_rules_xor(rule, mirror, copy_graph_1, 1)
                self.set_rules_xor(rule, mirror, copy_graph_2, 2)
        if prev_case == 4 or prev_case == 5:
            if case == 0 or case == 1:
                self.set_rules_xor(rule, node, copy_graph_1, 3)
                self.set_rules_xor(rule, node, copy_graph_2, 4)
            elif case == 2 or case == 7:
                self.set_rules_xor(rule, mirror, copy_graph_1, 3)
                self.set_rules_xor(rule, mirror, copy_graph_2, 4)
        if prev_case == 6:
            if case == 0 or case == 1 or case == 6:
                self.set_rules_xor(rule, node, copy_graph_1, 1)
                self.set_rules_xor(rule, node, copy_graph_2, 2)
            elif case == 2 or case == 7:
                self.set_rules_xor(rule, mirror, copy_graph_1, 1)
                self.set_rules_xor(rule, mirror, copy_graph_2, 2)
        if prev_case == 7:
            if case == 0 or case == 1 or case == 6:
                self.set_rules_xor(rule, node, copy_graph_1, 1)
                self.set_rules_xor(rule, node, copy_graph_2, 2)
            elif case == 2 or case == 7:
                self.set_rules_xor(rule, mirror, copy_graph_1, 1)
                self.set_rules_xor(rule, mirror, copy_graph_2, 2)
        
        if case == 0:
            self.check_ind_rules(origin_graph, copy_graph_1, copy_rule, case)
            self.check_ind_rules(origin_graph, copy_graph_2, copy_rule, case)
        if case == 1 or case == 5 or case == 6:
            self.check_ind_rules(origin_graph, copy_graph_1, copy_rule, case)
            self.check_ind_rules(origin_graph, copy_graph_2, None, 0)
        if case == 2 or case == 7:
            self.check_ind_rules(origin_graph, copy_graph_1, copy_rule, case)
            self.check_ind_rules(origin_graph, copy_graph_2, None, 0)
        
    def handle_or(self, origin_graph, current_graph, prev_rule, prev_case, node, rule, mirror):
        if prev_case == 1 or prev_case == 2:
            self.add_recursively_rule(node, prev_rule)
            self.add_recursively_rule(mirror, prev_rule)
        for index in range(0, len(current_graph.list_copy_rule)):
            if node in current_graph.list_copy_rule[index]:
                self.add_recursively_rule(node, current_graph.list_copy_rule[index][0])
                self.add_recursively_rule(mirror, current_graph.list_copy_rule[index][0])
                del current_graph.list_copy_rule[index]
                prev_case = 4
                break
        copy_graph_1 = copy.deepcopy(current_graph)
        copy_graph_2 = copy.deepcopy(current_graph)
        copy_graph_3 = copy.deepcopy(current_graph)
        copy_rule = None
        case = 0
        
        
        if type(mirror).__name__ == "Node_condition" and type(node).__name__ == "Node_condition":
            case = 3
            if prev_case == 0 or prev_case == 3:
                copy_rule_1 = self.set_special_or(rule, node, current_graph, copy_graph_1, 1)
                self.check_ind_rules(origin_graph, copy_graph_1, copy_rule_1, 3)
                copy_rule_2 = self.set_special_or(rule, node, current_graph, copy_graph_2, 2)
                self.check_ind_rules(origin_graph, copy_graph_2, copy_rule_2, 3)
                copy_rule_3 = self.set_special_or(rule, node, current_graph, copy_graph_3, 4)
                self.check_ind_rules(origin_graph, copy_graph_3, copy_rule_3, 3)
            
            elif prev_case == 1 or prev_case == 2 or prev_case == 4 or prev_case == 5:
                copy_rule_1 = self.set_special_or(rule, node, current_graph, copy_graph_1, 3)
                self.check_ind_rules(origin_graph, copy_graph_1, copy_rule_1, 3)

                
        if type(mirror).__name__ == "Node_condition" and case != 3:
            copy_node = copy_graph_1.find_letter_in_implies(node.name)
            copy_rule = self.get_copy_rule(node, rule, copy_node, copy_graph_1)
            self.handle_neg(copy_rule, copy_node, 0)
            self.handle_neg(copy_rule, copy_node.or_dic[copy_rule[0]], 1)
            case = 1 
        if type(node).__name__ == "Node_condition" and case != 3:
            copy_node = copy_graph_1.find_letter_in_implies(mirror.name)
            copy_rule = self.get_copy_rule(mirror, rule, copy_node, copy_graph_1)
            self.handle_neg(copy_rule, copy_node, 0)
            self.handle_neg(copy_rule, copy_node.or_dic[copy_rule[0]], 1)
            case = 2
        
        if prev_case == 0:
            if case == 1 or case == 0:
                self.set_rules_or(rule, node, copy_graph_1, 1)
                self.set_rules_or(rule, node, copy_graph_2, 2)
                self.set_rules_or(rule, node, copy_graph_3, 4)
            elif case == 2:
                self.set_rules_or(rule, mirror, copy_graph_1, 1)
                self.set_rules_or(rule, mirror, copy_graph_2, 2)
                self.set_rules_or(rule, mirror, copy_graph_3, 4)
        if prev_case == 1:
            if case == 0 or case == 1:
                self.set_rules_or(rule, node, copy_graph_1, 3)
            elif case == 2:
                self.set_rules_or(rule, mirror, copy_graph_1, 3)
        if prev_case == 2:
            if case == 0 or case == 1:
                self.set_rules_or(rule, node, copy_graph_1, 3)
            elif case == 2:
                self.set_rules_or(rule, mirror, copy_graph_1, 3)
        if prev_case == 3:
            if case == 0 or case == 1:
                self.set_rules_or(rule, node, copy_graph_1, 1)
                self.set_rules_or(rule, node, copy_graph_2, 2)
                self.set_rules_or(rule, node, copy_graph_3, 4)
            elif case == 2:
                self.set_rules_or(rule, mirror, copy_graph_1, 1)
                self.set_rules_or(rule, mirror, copy_graph_2, 2)
                self.set_rules_or(rule, mirror, copy_graph_3, 4)
        if prev_case == 4:
            if case == 0 or case == 1:
                self.set_rules_or(rule, node, copy_graph_1, 3)
            elif case == 2:
                self.set_rules_or(rule, mirror, copy_graph_1, 3)
        if prev_case == 5:
            if case == 0 or case == 1:
                self.set_rules_or(rule, node, copy_graph_1, 4)
            elif case == 2:
                self.set_rules_or(rule, mirror, copy_graph_1, 4)
        if case == 0:
            if prev_case == 0 or prev_case == 3:
                self.check_ind_rules(origin_graph, copy_graph_1, copy_rule, case)
                self.check_ind_rules(origin_graph, copy_graph_2, copy_rule, case)
                self.check_ind_rules(origin_graph, copy_graph_3, copy_rule, case)
            elif prev_case == 1 or prev_case == 2 or prev_case == 4 or prev_case == 5:
                self.check_ind_rules(origin_graph, copy_graph_1, copy_rule, case)
            
        if case == 1:
            if prev_case == 0 or prev_case == 3:
                self.check_ind_rules(origin_graph, copy_graph_1, copy_rule, case)
                self.check_ind_rules(origin_graph, copy_graph_2, None, 0)
                self.check_ind_rules(origin_graph, copy_graph_3, None, 0)
            elif prev_case == 1 or prev_case == 2 or prev_case == 4 or prev_case == 5:
                self.check_ind_rules(origin_graph, copy_graph_1, copy_rule, case)
        if case == 2:
            if prev_case == 0 or prev_case == 3:
                self.check_ind_rules(origin_graph, copy_graph_1, copy_rule, case)
                self.check_ind_rules(origin_graph, copy_graph_2, None, 0)
                self.check_ind_rules(origin_graph, copy_graph_3, None, 0)
            elif prev_case == 1 or prev_case == 2 or prev_case == 4 or prev_case == 5:
                self.check_ind_rules(origin_graph, copy_graph_1, copy_rule, case)
        
    def check_ind_rules(self, origin_graph, current_graph, prev_rule, prev_case):
        tot = 0
        
        for node in current_graph.ast_list:
            tot = self.crawl_ast(node, origin_graph, current_graph, prev_rule, prev_case)
            if tot != 0:
                return
        if tot == 0:
            origin_graph.list_copy.append(current_graph)

    
    def crawl_ast(self, node, origin_graph, current_graph, prev_rule, prev_case):
        if node:
            for rule, mirror in node.xor_dic.items():
                self.handle_xor(origin_graph, current_graph, prev_rule, prev_case, node, rule, mirror)
                return 1
            for rule, mirror in node.or_dic.items():
                self.handle_or(origin_graph, current_graph, prev_rule, prev_case, node, rule, mirror)
                return 1
            
            if type(node).__name__ == "Node_condition":
                if node.neg == 1 and prev_case == 0:
                    prev_case = 5
                if self.crawl_ast(node.left, origin_graph, current_graph, prev_rule, prev_case) == 1:
                    return 1
                return self.crawl_ast(node.right, origin_graph, current_graph, prev_rule, prev_case)
            return 0
    
    def set_special_xor(self, rule, node, current_graph, copy_graph, step):
        copy_node = self.get_copy_cond(node, current_graph, copy_graph)
        copy_rule = self.get_copy_rule_cond(node, rule, copy_node, copy_graph)
        copy_mirror = copy_node.xor_dic[copy_rule[0]]
        self.handle_neg(copy_rule, copy_node, 0)
        self.handle_neg(copy_rule, copy_mirror, 1)

        if step == 1:
            self.del_rule_in_childs(copy_mirror, copy_rule)
            copy_graph.list_copy_rule.append([copy_rule, copy_mirror.left, copy_mirror.right])
        if step == 2:
            self.del_rule_in_childs(copy_node, copy_rule)
            copy_graph.list_copy_rule.append([copy_rule, copy_node.left, copy_node.right])
        if step == 3:
            self.del_rule_in_childs(copy_mirror, copy_rule)
            self.del_rule_in_childs(copy_node, copy_rule)
            copy_graph.list_copy_rule.append([copy_rule, copy_mirror.left, copy_mirror.right])
            copy_graph.list_copy_rule.append([copy_rule, copy_node.left, copy_node.right])
        if step == 4:
            pass
        copy_mirror.xor_dic.pop(copy_rule[0])
        copy_node.xor_dic.pop(copy_rule[0])
        return copy_rule, copy_node
    
    def set_special_or(self, rule, node, current_graph, copy_graph, step):
        copy_node = self.get_copy_cond(node, current_graph, copy_graph)
        copy_rule = self.get_copy_rule_cond(node, rule, copy_node, copy_graph)
        copy_mirror = copy_node.or_dic[copy_rule[0]]
        self.handle_neg(copy_rule, copy_node, 0)
        self.handle_neg(copy_rule, copy_mirror, 1)
        if step == 1:
            self.del_rule_in_childs(copy_mirror, copy_rule)
            copy_graph.list_copy_rule.append([copy_rule, copy_mirror.left, copy_mirror.right])
        if step == 2:
            self.del_rule_in_childs(copy_node, copy_rule)
            copy_graph.list_copy_rule.append([copy_rule, copy_node.left, copy_node.right])
        if step == 3:
            self.del_rule_in_childs(copy_mirror, copy_rule)
            self.del_rule_in_childs(copy_node, copy_rule)
            copy_graph.list_copy_rule.append([copy_rule, copy_mirror.left, copy_mirror.right])
            copy_graph.list_copy_rule.append([copy_rule, copy_node.left, copy_node.right])
        if step == 4:
            pass
        copy_mirror.or_dic.pop(copy_rule[0])
        copy_node.or_dic.pop(copy_rule[0])
        return copy_rule
    
    def set_rules_xor(self, rule, node, copy_graph, step):
        copy_node = copy_graph.find_letter_in_implies(node.name)
        copy_rule = self.get_copy_rule(node, rule, copy_node, copy_graph)
        copy_mirror = copy_node.xor_dic[copy_rule[0]]
        self.handle_neg(copy_rule, copy_node, 0)
        self.handle_neg(copy_rule, copy_mirror, 1)
        if step == 1:
            self.del_rule_in_childs(copy_mirror, copy_rule)
        if step == 2:
            self.del_rule_in_childs(copy_node, copy_rule)
        if step == 3:
            self.del_rule_in_childs(copy_mirror, copy_rule)
            self.del_rule_in_childs(copy_node, copy_rule)
        copy_mirror.xor_dic.pop(copy_rule[0])
        copy_node.xor_dic.pop(copy_rule[0])

    def set_rules_or(self, rule, node, copy_graph, step):
        copy_node = copy_graph.find_letter_in_implies(node.name)
        copy_rule = self.get_copy_rule(node, rule, copy_node, copy_graph)      
        copy_mirror = copy_node.or_dic[copy_rule[0]]
        self.handle_neg(copy_rule, copy_node, 0)
        self.handle_neg(copy_rule, copy_mirror, 1)

        if step == 1:
            self.del_rule_in_childs(copy_mirror, copy_rule)
        if step == 2:
            self.del_rule_in_childs(copy_node, copy_rule)
        if step == 3:
            self.del_rule_in_childs(copy_mirror, copy_rule)
            self.del_rule_in_childs(copy_node, copy_rule)
        if step == 4:
            pass
        
        copy_mirror.or_dic.pop(copy_rule[0])
        copy_node.or_dic.pop(copy_rule[0])
    
    def del_rule_in_childs(self, node, rule):
        if node in rule[1]:
            if type(node).__name__ == "Node_letter":
                for index in range(0, len(node.childs_neg)):
                    if node.childs_neg[index] == rule[0]:
                        del node.childs_neg[index]
                        if rule[0] not in node.childs_pos:
                            node.childs_pos.append(rule[0])
                        return
            else:
                self.delete_recursively_rule(node, rule)
        else:
            if type(node).__name__ == "Node_letter":
                for index in range(0, len(node.childs_pos)):
                    if node.childs_pos[index] == rule[0]:
                        del node.childs_pos[index]
                        return
            else:
                self.delete_recursively_rule(node, rule)
                
    def delete_recursively_rule(self, node, rule):
        if node:
            if type(node).__name__ == "Node_letter":
                self.del_rule_in_childs(node, rule)
            if type(node).__name__ == "Node_condition":
                self.delete_recursively_rule(node.left, rule)
                self.delete_recursively_rule(node.right, rule)
                
    def add_recursively_rule(self, node, rule):
        if node:
            if type(node).__name__ == "Node_letter":
 
                if node in rule[1]:
                    node.childs_neg.append(rule[0])
                    self.del_rule_in_childs(node, [rule[0], []])
                else:
                    node.childs_pos.append(rule[0])
            if type(node).__name__ == "Node_condition":
                self.add_recursively_rule(node.left, rule)
                self.add_recursively_rule(node.right, rule)
                
    def get_copy_rule(self, true_node, true_rule, copy_node, copy_graph):
        for index in range(0, len(true_node.childs_pos)):
            if true_node.childs_pos[index] == true_rule:
                return [copy_node.childs_pos[index], []]
        for index in range(0, len(true_node.childs_neg)):
            if true_node.childs_neg[index] == true_rule:
                return [copy_node.childs_neg[index], []]
        return 
    
    def get_copy_rule_cond(self, node, rule, copy_node, copy_graph):
        while type(node).__name__ == "Node_condition":
            node = node.left
            copy_node = copy_node.left
        return self.get_copy_rule(node, rule, copy_node, copy_graph)
        
    def get_copy_cond(self, node, current_graph, copy_graph):
        
        for i in range(0, len(current_graph.ast_list)):
            ret = self.find_cond_in_ast(node, current_graph.ast_list[i], copy_graph.ast_list[i])
            if ret:
                return ret
            
    def find_cond_in_ast(self, to_find, root, copy_root):
        if root:
            if to_find == root:
                return copy_root
            if type(root).__name__ == "Node_condition":
                ret = self.find_cond_in_ast(to_find, root.left, copy_root.left)
                if ret:
                    return ret
                return self.find_cond_in_ast(to_find, root.right, copy_root.right)
        return None
    
    def handle_neg(self, copy_rule, node, pos):
        if type(node).__name__ == "Node_letter":
            if copy_rule[0] in node.childs_neg :
                copy_rule[1].append(node)
        if type(node).__name__ == "Node_condition":
            self.handle_neg(copy_rule, node.left, pos)
            self.handle_neg(copy_rule, node.right, pos)

    def display_table(self):
        print("Truth Tables")
        print('|', end="")
        for k in self.full_history.keys():
            print("    {}   |".format(k), end="")
        print()
        for hist in self.list_copy:
            print("|", end="")
            for v in hist.full_history.values():
                if v == True:
                    print("\033[92m  True  \033[0m|", end="")
                else:
                    print("\033[91m  False \033[0m|", end="")
            print()
        print("Result :")
        print("|", end="")
        for v in self.full_history.values():
            if v == True:
                print("\033[92m  True  \033[0m|", end="")
            elif v == False:
                print("\033[91m  False \033[0m|", end="")
            else:
                print("\033[93m   IND  \033[0m|", end="")
        print("\n")
