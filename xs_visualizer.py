import matplotlib.pyplot as plt
from networkx import draw_networkx_edges, draw_networkx_labels, \
                        draw_networkx_nodes, DiGraph, circular_layout


class Visualizer():

    def __init__(self):
        self.di_graph = None
        self.op_nodes = {}
        self.letter_nodes = []

    def get_node_name(self, node):
        if type(node).__name__ == "Node_letter":
            return node.token.value
        node_id = hex(id(node))
        if node.token.value not in self.op_nodes:
            self.op_nodes[node.token.value] = []
        if node_id not in self.op_nodes[node.token.value]:
            self.op_nodes[node.token.value].append(node_id)
        idx = self.op_nodes[node.token.value].index(node_id)
        if idx > 0:
            tmp = "{}{}".format(idx, node.token.value)
        else:
            tmp = node.token.value
        return tmp

    def image_run_graph(self, node, graph):
        if not node:
            return
        node.visited = 1
        if type(node).__name__ == "Node_letter":
            if node.token.value not in self.letter_nodes:
                self.letter_nodes.append(node.token.value)
            self.di_graph.add_node(node.token.value)
            implies_node = graph.find_letter_in_implies(node.name)
            if not implies_node:
                return
            for child in implies_node.childs_pos:
                if child.visited != 0:
                    continue
                tmp = self.get_node_name(child)
                tmp2 = self.get_node_name(implies_node)
                self.di_graph.add_edge(tmp, tmp2, weight=1)
                self.image_run_graph(child, graph)
            for child in implies_node.childs_neg:
                tmp = self.get_node_name(child)
                tmp2 = self.get_node_name(implies_node)
                self.di_graph.add_edge(tmp, tmp2, weight=0)
                self.image_run_graph(child, graph)

        if type(node).__name__ == "Node_condition":
            self.di_graph.add_node(node.token.value)
            tmp = self.get_node_name(node)
            t1 = self.get_node_name(node.left)
            t2 = self.get_node_name(node.right)
            w1 = 0 if node.left.neg == 1 else 1
            w2 = 0 if node.right.neg == 1 else 1
            self.image_run_graph(node.left, graph)
            self.di_graph.add_edge(t1, tmp, weight=w1)
            self.di_graph.add_edge(t2, tmp, weight=w2)
            self.image_run_graph(node.right, graph)
        node.visited = 0

    def generate_graph(self, node, graph):
        val = node.token.value
        self.image_run_graph(node, graph)

        pos = circular_layout(self.di_graph)
        draw_networkx_nodes(self.di_graph, pos)

        g_nodes = []
        for k, v in self.op_nodes.items():
            g_nodes.append(k)
            for i in range(1, len(v)):
                g_nodes.append("{}{}".format(i, k))
        e_pos = ([(u, v) for (u, v, d) in self.di_graph.edges(data=True)
                 if d['weight'] == 1])
        e_neg = ([(u, v) for (u, v, d) in self.di_graph.edges(data=True)
                 if d['weight'] == 0])

        draw_networkx_edges(self.di_graph, pos,
                            edgelist=e_pos,
                            arrowstyle='->')
        draw_networkx_edges(self.di_graph, pos,
                            edgelist=e_neg,
                            arrowstyle='->',
                            edge_color='firebrick')
        draw_networkx_nodes(self.di_graph, pos,
                            nodelist=g_nodes,
                            node_color='cornflowerblue')

        draw_networkx_nodes(self.di_graph, pos,
                            nodelist=self.letter_nodes,
                            node_color='lightcoral')
        if val:
            draw_networkx_nodes(self.di_graph, pos,
                                nodelist=[val],
                                node_color='mediumseagreen')
        draw_networkx_labels(self.di_graph, pos,
                             font_size=12,
                             font_family='sans-serif',
                             arrowsize=50,
                             arrowstyle='->')
        plt.axis('off')
        plt.savefig("{}_graph.png".format(val))
        plt.close()

    def generate_all_graphs(self, facts_list, graph):
        for letter in facts_list:
            self.op_nodes = {}
            self.letter_nodes = []
            self.di_graph = DiGraph()
            node = graph.find_letter_in_implies(letter)
            if node is None:
                print("{} not in implies, "
                      "stopping image generation ...".format(letter))
                continue
            self.generate_graph(node, graph)
