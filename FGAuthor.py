from networkx.algorithms import bipartite

from pylab import *
import networkx as nx
import pandas as pd
import matplotlib.lines as mlines
from operator import itemgetter
import multiprocessing

def FGAfunc():
    # Open input csv file, and create output files
    dataset = pd.read_csv('Data/frequencyTest.csv', delimiter=',')
    topologyStatisticsFile = open("topologyStatistics.txt", 'w', encoding='utf8')
    graphDictionaryFile = open("graphDictionary.txt", 'w', encoding='utf8')
    appList = []

    # Find list of all apps commented on
    for i in range(dataset['App'].count()):
        splitVal = dataset['App'][i].split(';')
        for j in range(len(splitVal)):
            appList.append(splitVal[j])

    # Remove redundant entries, and put into a dictionary with a base comment score of 0
    appList = set(appList)
    appList = list(appList)
    appList = {i: 0 for i in appList}
    authList = {}

    # Create dictionary for author values. Including name, apps commented on, and number of apps commented on
    for i in range(dataset['Author'].count()):
        aVal1 = dataset['Author'][i]
        aVal2 = dataset['App'][i]
        aVal3 = dataset['Total'][i]
        authList[aVal1] = aVal2, aVal3

    # Create and name graph
    G = nx.Graph()
    H = nx.Graph()
    G.name = "Topological Network Analysis"

    # Add author list and apps list
    H.add_nodes_from(authList.keys())
    G.add_nodes_from(appList.keys(), bipartite=0)
    G.add_nodes_from(authList.keys(), bipartite=1)

    # Add edge between every author and every app they commented on
    for key, value in authList.items():
        for k, v in appList.items():
            if k in authList[key][0]:
                G.add_edge(key, k, weight=0.25)
                appList[k] += 1

    o = list(G.edges)

    jc = nx.jaccard_coefficient(G)
    #print(jc)

    #G.remove_edges_from(list(G.edges()))

    #print(G)

    #print(appList.items())
    #print(jc)

    #for u, v, p in jc:
        #for k in appList.items():
            #print(appList[k])
            #if u in appList[k][0]:
                #jc.remove(u)

    #print(appList)
    #H.remove_edges_from(appList)

    widthVal = []

    for u, v, p in jc:

        widthVal.append(float(p))

        #print(u, v, p)
        sp = float(p)
        #print(sp)
        if sp > 0.0:
            #print(sp)
            #print("yes!!!!!!!!!!!!!!!!")
            H.add_edge(u, v, weight=sp*20)

    H.remove_edges_from(appList)

    #for k in knn:
        #if k in authList[key][0]:
            #G.add_edge(key, k, weight=0.25)
            #appList[k] += 1

    #print(o)

    #print(H.edges(appList[0]))

    #for y, g in appList.items():
        #H.remove_edge(H.edges(appList.keys()))

    H.remove_nodes_from(appList.keys())

    #print(G.edges)

    # Print statistical information
    print(nx.info(H))
    topologyStatisticsFile.write(str(nx.info(H))+"\n")
    density = nx.density(H)
    print("Network density:", density)
    topologyStatisticsFile.write("Network density: "+str(density))
    degree_dict = dict(H.degree(H.nodes()))
    nx.set_node_attributes(H, degree_dict, 'degree')
    sorted_degree = sorted(degree_dict.items(), key=itemgetter(1), reverse=True)
    print("Top 5 nodes by degree:")
    for d in sorted_degree[:5]:
        print(d)

    # Determine node size
    #appWeight = [float(l)*50 for x,l in appList.items()]
    #authWeight = [l for x,l in authList.items()]
    #print(authList.items())
    authWeight = [float(l[1])*50 for x,l in authList.items()]
    #print(authWeight)

    #print(H.edges)

    # Map to layout
    pos = nx.spring_layout(H, k=0.25, iterations=70, scale=10)
    print(H.size())
    plt.figure(1, figsize=(100,100))


    #print("yo = "+str(size(authList.keys())))
    #print(size(authWeight))


    # Draw network
    #nx.draw_networkx_nodes(H, pos=pos, node_color="red", nodelist=appList.keys(), node_size=appWeight)
    nx.draw_networkx_nodes(H, pos=pos, node_color="blue", nodelist=authList.keys(), node_size=authWeight)
    nx.draw_networkx_edges(H, pos=pos, width=widthVal)

    # Add legend
    p = mlines.Line2D([],[],label="Author",color="blue")
    a = mlines.Line2D([],[],label="Application",color="red")
    plt.legend(handles=[p,a])

    print(multiprocessing.cpu_count())
    # Print graph list to output, and output image
    graphDictionaryFile.write(str(H.edges))
    plt.savefig("FoldedGraphAnalysis.jpg")

    # Return graph to call function
    return H
