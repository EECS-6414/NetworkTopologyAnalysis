from collections import Counter

import networkx as nx


def generateDegreeHistogram(G, key):
    """Returns a list of the frequency of each degree value.

    Parameters
    ----------
    G : Networkx graph
       A graph

    Returns
    -------
    hist : list
       A list of frequencies of degrees.
       The degree values are the index in the list.

    Notes
    -----
    Note: the bins are width one, hence len(list) can be large
    (Order(number_of_edges))
    """

    global counts
    color = nx.get_node_attributes(G, "type")

    degreeDistribution = []
    for n, d in G.degree():
        if color[n] == key:
            degreeDistribution.append(d)

    counts = Counter(d for d in degreeDistribution)

    return [counts.get(i, 0) for i in range(max(counts) + 1)]
