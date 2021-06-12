import trieofrules.arm as arm
import networkx as nx
import matplotlib.pyplot as plt


class trieofrules:
    def __init__(self, data, min_support = 0.1, alg='FP-max',frequent_sequences = None,
                    round_value = 3):
        """
        init with raw data. it's neede for metrics
        Uses mlxtnd arm, so it may work badly with large-scale dataset
        TODO:
            rework for FP-growth and FP-max using norm library
        """
        self.data = data
        self.min_support = min_support
        self.alg = alg
        self.round_value = round_value
        if frequent_sequences is not None:
            self.frequent_sequences = frequent_sequences
            self.frequent_items = arm.find_frequent_items_by_sequencset(self.data, self.frequent_sequences)
        else:
            self.frequent_sequences = arm.mine_frequent_sequences(data, min_support, alg)
            self.frequent_items = arm.find_frequent_items(self.data, self.min_support)


        self.create_trie()
        self.add_metrics(self.root_node_id) #extend trie with ARM metrics starting from root


    def create_trie(self):
        """
        create actual Trie of rules
        """
        self.trie  = nx.DiGraph()
        self.trie.add_node(0, value='NULL')
        self.root_node_id = 0

        for sequence in self.frequent_sequences:
            sorted_items = []
            for el in self.frequent_items.keys():
                if el in sequence:
                    sorted_items.append(el)
            if len(sorted_items) > 0:
                self.insert_tree(sorted_items)


    def insert_tree(self,items):
        current_node_id = self.root_node_id
        for item in items:
            for children in self.trie.adj[current_node_id]:
                if (self.trie.nodes[children]['value']==item):
                    current_node_id = children
                    break
            else: #for-else, we didn't find this item, then create a new branch
                new_node_id = self.trie.number_of_nodes()
                self.trie.add_edge(current_node_id, new_node_id)
                self.trie.nodes[new_node_id]['value'] = item
                current_node_id = new_node_id

    def add_metrics(self,node_id):
        if node_id == 0:
            self.trie.nodes[node_id]['support'] = 1
            self.trie.nodes[node_id]['confidence'] = 1
            self.trie.nodes[node_id]['lift'] = 1
        else:
            rule = self.get_path(node_id)
            support = arm.get_support(rule, self.data)
            predecessor_id = list(self.trie.predecessors(node_id))[0]
            predecessor_support = self.trie.nodes[predecessor_id]['support']
            self.trie.nodes[node_id]['support'] = round(support, self.round_value)
            #conf(abc-d)=supp(abcd)/sup(abc)
            self.trie.nodes[node_id]['confidence'] = round(support/predecessor_support,self.round_value)
            #lift(abc-d) = supp(abcd)/supp(abc)supp(d)
            consequent = rule[-1] #last item
            consequent_support = self.frequent_items[consequent]/len(self.data)
            self.trie.nodes[node_id]['lift'] = round(support/(predecessor_support*consequent_support),self.round_value)

        for child in self.trie.adj[node_id]:
            self.add_metrics(child)



    def get_path(self,node_id):
        rule = []
        while node_id != self.root_node_id:
            rule.append(self.trie.nodes[node_id]['value'])
            node_id = list(self.trie.predecessors(node_id))[0] #take the only one predecessor
        return rule[::-1]

    def draw(self):
        labels = nx.get_node_attributes(self.trie, 'value')
        nx.draw_kamada_kawai(self.trie, with_labels=True, font_weight='bold', labels = labels)
