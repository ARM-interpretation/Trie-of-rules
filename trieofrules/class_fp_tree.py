import itertools
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.etree import ElementTree
from xml.dom import minidom


class FPNode(object):
    """
    A node in the FP tree.
    """

    def __init__(self, value, count, parent, id_counter):
        """
        Create the node.
        """

        self.value = value #name
        self.count = count
        self.parent = parent
        self.link = None
        self.children = []
        self.id= id_counter

    def has_child(self, value):
        """
        Check if node has a particular child node.
        """
        for node in self.children:
            if node.value == value:
                return True

        return False

    def get_child(self, value):
        """
        Return a child node with a particular value.
        """
        for node in self.children:
            if node.value == value:
                return node

        return None

    def add_child(self, value, id_counter):
        """
        Add a node as a child node.
        """
        child = FPNode(value, 1, self, id_counter)
        self.children.append(child)
        return child

    def get_branch(self, branch = None): # empty dict in default params is dangerous so None
        """
        recursevly creates dict with counters from a branch picked by node
        returns dict of items and summ count {'a':12,'b':2...}
        """

        if branch is None: #TODO delete this and find a way to overcome https://stackoverflow.com/questions/26320899/why-is-the-empty-dictionary-a-dangerous-default-value-in-python
            branch = {}

        if self.value in branch:
            branch[self.value] += self.count
        else:
            branch[self.value] = self.count
        #print(branch, fp_node.value)
        for children in self.children:
            children_branch = children.get_branch(branch)
            branch.update(children_branch)

        return branch

    def get_path(self):
        """
        returns path from the node to the root of the fp_tree
        returns list of items(names-value of nodes)
        """
        current_node = self
        path = []
        while current_node.parent != None:
            path.append(current_node.value)
            current_node = current_node.parent

        return path



class FPTree(object):
    """
    A frequent pattern tree.
    """
    def __init__(self, transactions, min_support, max_support = 1, root_value=None, root_count=None, frequent = None):
        """
        Initialize the tree.
        """
        if frequent is None:
            self.frequent = self.find_frequent_items(transactions, min_support, max_support)
        else:
             self.frequent = frequent
        self.headers = self.build_header_table(self.frequent)
        self.id_counter = 0
        self.root = self.build_fptree(
            transactions, root_value,
            root_count, self.frequent, self.headers)
        self.number_of_transactions = len(transactions)



    @staticmethod
    def find_frequent_items(transactions, min_support,max_support):
        """
        Create a dictionary of items with occurrences above and below the thresholds.
        """
        items = {}

        for transaction in transactions:
            for item in transaction:
                if item in items:
                    items[item] += 1
                else:
                    items[item] = 1

        for key in list(items.keys()):
            if items[key]/len(transactions) < min_support or items[key]/len(transactions)>max_support:
                del items[key]

        items = {k: v for k, v in sorted(items.items(), key=lambda item: item[1], reverse = True)}
        return items

    @staticmethod
    def build_header_table(frequent):
        """
        Build the header table.
        """
        headers = {}
        for key in frequent.keys():
            headers[key] = None

        return headers


    def build_fptree(self, transactions, root_value,
                     root_count, frequent, headers):
        """
        Build the FP tree and return the root node.
        """
        root = FPNode(root_value, root_count, None, self.id_counter)

        for transaction in transactions:
            # for some reasons this normal sorting gives different results
            # depending on how many items in the list. That is why for now
            # there is implementation of manual sorting of list according to
            # frequency of items
            #TODO find out why this function returns different results
            #sorted_items = [x for x in transaction if x in frequent]
            #sorted_items.sort(key=lambda x: frequent[x], reverse=True)

            sorted_items = []
            for el in frequent.keys():
                if el in transaction:
                    sorted_items.append(el)
            if len(sorted_items) > 0:
                self.insert_tree(sorted_items, root, headers)

        return root

    def insert_tree(self, items, node, headers):
        """
        Recursively grow FP tree.
        """
        first = items[0]
        child = node.get_child(first)
        if child is not None:
            child.count += 1
        else:
            # Add new child.
            self.id_counter += 1
            child = node.add_child(first,self.id_counter)


            # Link it to header structure.
            if headers[first] is None:
                headers[first] = child
            else:
                current = headers[first]
                while current.link is not None:
                    current = current.link
                current.link = child

        # Call function recursively.
        remaining_items = items[1:]
        if len(remaining_items) > 0:
            self.insert_tree(remaining_items, child, headers)

    def tree_has_single_path(self, node):
        """
        If there is a single path in the tree,
        return True, else return False.
        """
        num_children = len(node.children)
        if num_children > 1:
            return False
        elif num_children == 0:
            return True
        else:
            return True and self.tree_has_single_path(node.children[0])

    @staticmethod
    def _prettify(elem):
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ElementTree.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def write_graphml(self, filename = 'output', extended = False):
        """
        write FPTree as an XML file( .graphml )
        """
        #preamble
        top = Element('graphml')

        #attributes description
        attributes_list = {'value':'string', 'count':'integer'} #,'support':'double'} #attributes with its type
        if extended:
            attributes_list.update({'support':'double', 'confidence':'double','lift':'double'})

        for num, attribute in enumerate(attributes_list):
            key = SubElement(top, 'key',{
                'id': 'd' + str(num), #d0,d1,d2...
                'attr.name':attribute,
                'attr.type': attributes_list[attribute],
                'for':'node' #mark that these ara attributes for nodes
            })

        graph = SubElement(top, 'graph')
        graph.set('edgedefault','directed')
        #end of preamble

        #manually add root values

        root = SubElement(graph,'node',{'id':str(self.root.id)})
        SubElement(root,'data',{'key': 'd0'}).text = 'null' #name
        SubElement(root,'data',{'key': 'd1'}).text = str(self.number_of_transactions) #counter
        if extended:
            SubElement(root,'data',{'key': 'd2'}).text = str(self.root.support) #counter
            SubElement(root,'data',{'key': 'd3'}).text = str(self.root.confidence) #counter


        #add all nodes and edges ( self.headers - dict of stack of nodes)
        for el in self.headers:
            fp_node = self.headers[el]
            while fp_node is not None:
                node = SubElement(graph,'node',{
                    'id':str(fp_node.id)
                })
                #set attributes for this node
                for num,attribute in enumerate(attributes_list):
                    att = SubElement(node,'data',{
                        'key': 'd' + str(num)
                    })
                    att.text = str(getattr(fp_node,attribute))

                #set edge from parent to this node
                if extended:
                    edge = SubElement(graph, 'edge',{
                        'source':str(fp_node.parent.id),
                        'target':str(fp_node.id),
                        'Weight':str(fp_node.confidence*100)
                    })
                else:
                        edge = SubElement(graph, 'edge',{
                            'source':str(fp_node.parent.id),
                            'target':str(fp_node.id)
                        })

                fp_node = fp_node.link #go to the next node with the same name

        #file save
        with open( filename + ".graphml", "w") as file:
            file.write(FPTree._prettify(top))

    def get_node(self,id_value):
        """
        Returns node with given id_value
        """
        for el in self.headers:
            node = self.headers[el]
            while node is not None:
                if node.id==id_value:
                    return node
                node = node.link

        return None
