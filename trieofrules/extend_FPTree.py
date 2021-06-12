def get_support(search_list,dataset):
    """
    returns support value for the search list in the dataset
    search_list  - set of items
    dataset - list of lists
    returns double value (0.32312)
    """

    search_set = set(search_list)
    support_counter = 0
    for row in dataset:
        if search_set.issubset(set(row)):
            support_counter += 1
    return support_counter/len(dataset)


def extend_metrics_FPTree(fp_tree,dataset,round_value=3):
    """
    add metrics: support and confidence to fp_tree with respect to dataset
    Confidence of the node is the confidence for a rule that has as an consequent this node,
        and antecndent - path from root to the prvious node
    fp_tree - FPTree object
    dataset - list of lists #probably should be something else. This doesnt sound very efficient
    round_value - how many digiets left after dot x.zyx
    """
    fp_tree.root.support = 1
    fp_tree.root.confidence = 1
    fp_tree.root.lift = 1
    for el in fp_tree.headers:
            fp_node = fp_tree.headers[el]
            while fp_node is not None:
                fp_node.support = round(get_support(fp_node.get_path(),dataset),round_value)
                #confidence of the node is support of the node devided by the support of the parrent node.
                #conf(abc-d)=supp(abcd)/sup(abc)
                fp_node.confidence = round(fp_node.support/fp_node.parent.support,round_value)
                #lift(abc-d) = supp(abcd)/supp(abc)supp(d)
                consequent_support = get_support([fp_node.value],dataset)
                fp_node.lift = round(fp_node.support/(fp_node.parent.support*consequent_support),round_value)

                #print(fp_node.get_path()[::-1], fp_node.confidence)
                fp_node = fp_node.link #go to the next node with the same name
