from trieofrules import trieofrules

#original dataset
data = [
        ['f','c','a','m','p','q'],
        ['f','c','a','b','m'],
        ['f','b','e'],
        ['c','b','p'],
        ['f','c','a','m','p'] ]

#association rules for visualisation presented as a list of frequent sequences
rules = [['f','c','a','m','p'],
        ['f','b'],
        ['c','b'],
        ['f','c','q']
        ]

#1st approcah using only data
TOR = trieofrules(data = data, min_support = 0.3, alg='FP-max' ) #supported algorithms: FP-max, FP-growth, Apriori

#2nd approach using data and pre-mined frequent sequences
TOR_premined = trieofrules(data = data, alg = 'Apriori', frequent_sequences = rules)

#draw trie of rules without metics
TOR_premined.draw()

#save as a grpah file. Supprted formats: gexf, gml, graphml
TOR.save_graph(filename = 'test.gml',fileformat = 'gml')
