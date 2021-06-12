import networkx as nx
import matplotlib.pyplot as plt

class trie:
    def __init__(self,frequent_sequences, frequent_items):
        self.graph  = nx.DiGraph()
        self.graph.add_node(0, value='NULL')


        for sequence in frequent_sequences:
            sorted_items = []
            for el in frequent_items.keys():
                if el in sequence:
                    sorted_items.append(el)
            if len(sorted_items) > 0:
                self.insert_tree(sorted_items)



    def insert_tree(self,items):
        current_node_id = 0 #root
        for item in items:
            for children in self.graph.adj[current_node_id]:
                if (self.graph.nodes[children]['value']==item):
                    current_node_id = children
                    break
            else: #for-else, we didn't find this item, then create a new branch
                new_node_id = self.graph.number_of_nodes()
                self.graph.add_edge(current_node_id, new_node_id)
                self.graph.nodes[new_node_id]['value'] = item
                current_node_id = new_node_id

    def add_metrics(self):


    def draw(self):
        labels = nx.get_node_attributes(self.graph, 'value')
        nx.draw_kamada_kawai(self.graph, with_labels=True, font_weight='bold', labels = labels)
