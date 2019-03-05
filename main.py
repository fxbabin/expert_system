from xs_graph import Graph
from xs_parser import Parser
from xs_lexer import Lexer
from xs_setting import Setting


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

        for queried in setting.queries:
            graph.query(queried)

    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
