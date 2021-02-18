from pylab import *
import networkx as nx
import pandas as pd
import matplotlib.lines as mlines
from operator import itemgetter

def TNAfunc():
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
    G.name = "Topological Network Analysis"

    # Add author list and apps list
    G.add_nodes_from(appList.keys())
    G.add_nodes_from(authList.keys())

    # Add edge between every author and every app they commented on
    for key, value in authList.items():
        for k, v in appList.items():
            if k in authList[key][0]:
                G.add_edge(key, k, weight=0.25)
                appList[k] += 1

    # Print statistical information
    print(nx.info(G))
    topologyStatisticsFile.write(str(nx.info(G))+"\n")
    density = nx.density(G)
    print("Network density:", density)
    topologyStatisticsFile.write("Network density: "+str(density))
    degree_dict = dict(G.degree(G.nodes()))
    nx.set_node_attributes(G, degree_dict, 'degree')
    sorted_degree = sorted(degree_dict.items(), key=itemgetter(1), reverse=True)
    print("Top 5 nodes by degree:")
    for d in sorted_degree[:5]:
        print(d)

    # Determine node size
    appWeight = [float(l)*50 for x,l in appList.items()]
    authWeight = [l for x,l in authList.items()]
    authWeight = [float(l)*50 for x,l in authWeight]
    print("Weights assigned")

    # Map to layout
    pos = nx.spring_layout(G, k=0.25, iterations=70, scale=10)
    print(G.size())
    plt.figure(3,figsize=(200,200))

    # Draw network
    nx.draw_networkx_nodes(G, pos=pos, node_color="red", nodelist=appList.keys(), node_size=appWeight)
    nx.draw_networkx_nodes(G, pos=pos, node_color="blue", nodelist=authList.keys(), node_size=authWeight)
    nx.draw_networkx_edges(G, pos=pos)

    # Add legend
    p = mlines.Line2D([],[],label="Author",color="blue")
    a = mlines.Line2D([],[],label="Application",color="red")
    plt.legend(handles=[p,a])

    # Print graph list to output, and output image
    graphDictionaryFile.write(str(G.edges))
    plt.savefig("TopologicalAnalysis.jpg")

    # Return graph to call function
    return G