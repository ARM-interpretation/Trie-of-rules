from trieofrules import trieofrules

"""
general test:
creates sample dataset
creates trie
"""
data = [
        ['f','c','a','m','p','q'],
        ['f','c','a','b','m'],
        ['f','b','e'],
        ['c','b','p'],
        ['f','c','a','m','p'] ]

rules = [['f','c','a','m','p'],
        ['f','b'],
        ['c','b']]


#trie = trieofrules(data,0.1,'Apriori',rules)
trie = trieofrules(data,0.3)
print(trie.trie)
