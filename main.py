from xs_graph import Graph
from xs_parser import Parser
from xs_lexer import Lexer
from xs_setting import Setting


def process_engine(setting):
    if setting.graph_rules:
        try:
            print('Importing visualizer (this may take some time) ...')
            from xs_visualizer import Visualizer
        except ImportError:
            raise ImportError('Failed to import visualizer')
    try:
        graph = Graph()
        for rule in setting.rules:
            graph.add_new_AST(Parser(Lexer(rule)).parse())

        graph.learn_facts(setting.true_facts)

        for node in graph.implies_list:
            graph.set_facts(node)

        if setting.graph_rules:
            visu = Visualizer()
            visu.generate_all_graphs(setting.graph_rules, graph)

        graph.display_tables = setting.truth_tables
        if graph.incoherent == 0:
            graph.resolve_simple()
        else:
            graph.resolve_complex()

        for queried in setting.queries:
            graph.query(queried)

    except Exception as e:
        print(e)

def ask_new_facts(setting):
    entry = input("Previous facts where : {}\nEnter the new facts please ('x' to quit)\n".format(setting.true_facts))
    if entry == "x":
        print("Good bye")
        setting.interactive = False
        return
    for l in entry:
        if ord(l) < 65 or ord(l) > 90:
            print("Please enter only valid facts")
            ask_new_facts(setting)
    setting.true_facts = entry

def main():
    setting = Setting()
    if setting.interactive:
        while setting.interactive:
            process_engine(setting)
            ask_new_facts(setting)
    else:
        process_engine(setting)

if __name__ == "__main__":
    main()
