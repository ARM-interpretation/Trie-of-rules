from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpmax,apriori,fpgrowth
from mlxtend.frequent_patterns import association_rules
import pandas as pd

def mine_frequent_sequences(transactions, min_support,alg,min_len):
    arm_alg = {'FP-max':fpmax, 'Apriori':apriori, 'FP-rowth':fpgrowth}
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    frequent_sequences = arm_alg[alg](df, min_support, use_colnames=True).itemsets.tolist()
    return [set(x) for x in frequent_sequences if len(set(x))>=min_len]

def find_frequent_items(transactions, min_support):
    """
    Create a dictionary of items with occurrences above the thresholds.
    """
    items = {}

    for transaction in transactions:
        for item in transaction:
            if item in items :
                items[item] += 1
            else:
                items[item] = 1

    number_of_transactions = len(transactions)
    for key in list(items.keys()):
        if items[key]/number_of_transactions < min_support:
            del items[key]

    items = {k: v for k, v in sorted(items.items(), key=lambda item: item[1], reverse = True)}
    return items


def find_frequent_items_by_sequencset(transactions, frequent_sequences):
    """
    Create a dictionary of items that are part of frequent frequent_sequences
    and get their support values
    """
    items = {}

    for sequence in frequent_sequences:
        for item in sequence:
            if item not in items:
                items[item]=0

    for transaction in transactions:
        for item in transaction:
            if item in items:
                items[item] += 1


    items = {k: v for k, v in sorted(items.items(), key=lambda item: item[1], reverse = True)}
    return items

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
