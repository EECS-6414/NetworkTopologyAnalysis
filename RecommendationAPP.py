from collections import Counter
from operator import itemgetter

import networkx as nx


def RecommendApp(author):
    # read graph from disk
    global listForThisAuthor
    G_APP = nx.read_gpickle("graphs/G_APP.gpickle")
    G_Complete = nx.read_gpickle("graphs/G_COMPLETE.gpickle")

    degree_dict = dict(G_Complete.degree(G_Complete.nodes()))
    nx.set_node_attributes(G_Complete, degree_dict, 'degree')
    sorted_degree = sorted(degree_dict.items(), key=itemgetter(1), reverse=False)
    listAuthorRank = []
    listRecommendation = []
    listRecommendationA = []
    print("\n\n------------Processing author: " + author)
    listForThisAuthor = []
    parts = str(G_Complete.edges(author)).split("\')")
    for p in range(0, len(parts) - 1):
        secondPart = parts[p].split("\',")
        listForThisAuthor.append(secondPart[1].replace(" \'", ""))
    listAppUse, listAppTest = split_list(listForThisAuthor)
    for a in listAppUse:
        edgesSorted = sorted(G_APP[a].items(), key=lambda edge: edge[1]['weight'])
        # for k in range(len(edgesSorted)-6, len(edgesSorted)-1):
        # print("jaime: "+edgesSorted[k][0]+": "+str(edgesSorted[k][1]["weight"]))
        # print("\nTesting APP this author has:")
        weight = 0
        for all in listAppTest:
            for k in edgesSorted:
                if k[0] == all:
                    # print(k[0] + ": " + str(k[1]["weight"]))
                    weight += k[1]["weight"]
        weightA = weight / len(listAppTest)
        # print("average: "+str(weightA))
        # print("\nRecomendation:  ")
        for k in range(len(edgesSorted) - 14, len(edgesSorted) - 1):
            weight = (edgesSorted[k][1]["weight"] + weightA) / 2
            # print(edgesSorted[k][0]+": "+str(weight))
            tuple1 = (edgesSorted[k][0], weight)
            listAuthorRank.append(tuple1)
        listAuthorRank.sort(reverse=True, key=myFunc)
    print("\n--> Top 5 recommendation for this Author: ")
    # print("\n--> before: ")
    # for i in range(0, 10):
    #     print(listAuthorRank[i])
    listNewOne = []
    for i in range(0, 13):
        listNewOne.append(listAuthorRank[i])
    newListFinal = []

    for i in range(0, len(listNewOne) - 1):
        weight = listNewOne[i][1]
        for j in range(0, len(listNewOne) - 1):
            if j != i and listNewOne[i][0] == listNewOne[j][0]:
                weight += listNewOne[j][1]
        tuple1 = (listNewOne[i][0], weight)
        newListFinal.append(tuple1)

    newListFinal.sort(reverse=True, key=myFunc)
    newListFinal = list(dict.fromkeys(newListFinal))
    for i in range(0, 5):
        print(newListFinal[i])
    print("This author has: " + str(G_Complete.edges(author)))


def split_list(a_list):
    half = len(a_list) // 2
    return a_list[:half], a_list[half:]


def myFunc(e):
    return e[1]
