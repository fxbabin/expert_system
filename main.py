from Graph import Graph
from Interpreter import Interpreter
from es_parser import Parser
from es_lexer import Lexer
from es_token import Token
from es_node import Node_letter, Node_condition
from es_setting import Setting
import argparse


def main():
    setting = Setting()
    try:
        graph = Graph()
        for rule in setting.rules:
            graph.add_new_AST(Parser(Lexer(rule)).parse())
    
        graph.learn_facts(setting.true_facts)
        
        for node in graph.implies_list:
            graph.set_facts(node)
        
        graph.check_contradiction()
    
#        for node in graph.implies_list[3].childs_pos:
#            print(node.left.left.right)
        for queried in setting.queries:
            graph.query(queried)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
