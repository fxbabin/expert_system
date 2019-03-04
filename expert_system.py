from Graph import Graph
from Interpreter import Interpreter
from Lexer import Lexer
from Parser import Parser
from ast import Token, Node_condition, Node_letter

def main():
    rule1 = "A => B"
    rule2 = "B => C"
    rule3 = "C => !A"

    true_facts = "C"

    try:
        graph = Graph()
    
        root1 = Parser(Lexer(rule1)).parse()
        graph.add_new_AST(root1)
    
        root2 = Parser(Lexer(rule2)).parse()
        graph.add_new_AST(root2)
        
        root3 = Parser(Lexer(rule3)).parse()
        graph.add_new_AST(root3)
    
#     root4 = Parser(Lexer(rule4)).parse()
#     graph.add_new_AST(root4)
    
        graph.learn_facts(true_facts)
    
        for node in graph.implies_list:
            graph.set_facts(node)
    
        graph.check_contradiction()
    
        graph.query("A")
        graph.query("B")
        graph.query("C")
#     graph.query("F")


    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
