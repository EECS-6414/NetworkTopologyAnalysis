
import pandas
from pylab import *
import networkx as nx
import pandas as pd
import matplotlib.lines as mlines
from operator import itemgetter
from fileNames import files

def TNAfunc():
    # Open input csv file, and create output files
    dataset = pd.read_csv('frequency.csv', delimiter=',')
    appNamesFile = pd.read_csv('apps_names.csv', delimiter=',')

    topologyStatisticsFile = open("topologyStatistics.txt", 'w', encoding='utf8')
    graphDictionaryFile = open("graphDictionary.txt", 'w', encoding='utf8')
    appList = []
    appRawList = []
    listWithAllAppsHash = []

    print("getting apps...")
    for i in range(dataset['App'].count()):
        splitVal = dataset['App'][i].split(';')
        for j in range(len(splitVal)):
            appList.append(splitVal[j])

    for i in range(appNamesFile['App'].count()):
        appRawList.append(appNamesFile['App'][i])


    # Remove redundant entries, and put into a dictionary with a base comment score of 0
    appList = set(appList)

    # check if name of app is valid
    for e in appList:
        if e in appRawList:
            listWithAllAppsHash.append(e)

    listWithAllAppsHash = list(listWithAllAppsHash)
    listWithAllAppsHash = {i: 0 for i in listWithAllAppsHash}
    authListHash = {}

    # Create dictionary for author values. Including name, apps commented on, and number of apps commented on
    print("getting comments...")
    for i in range(dataset['Author'].count()):
        aVal1 = dataset['Author'][i]
        aVal2 = dataset['App'][i]
        aVal3 = dataset['Total'][i]
        authListHash[aVal1] = aVal2, aVal3

    # Create and name graph
    G = nx.Graph()
    G.name = "Topological Network Analysis"

    # Add author list and apps list
    G.add_nodes_from(listWithAllAppsHash.keys())
    G.add_nodes_from(authListHash.keys())

    #for key, item in authListHash:




    # Add edge between every author and every app they commented on
    print("building network (2 min)...")
    for key, value in authListHash.items():
        for k, v in listWithAllAppsHash.items():
            if k in authListHash[key][0]:
                G.add_edge(key, k, weight=0.25)
                listWithAllAppsHash[k] += 1

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
    topologyStatisticsFile.write("top 10 Apps:")
    for d in sorted_degree[:10]:
        print(d)
        topologyStatisticsFile.write(str(d)+"\n")

    # Determine node size
    appWeight = [float(l)*50 for x,l in listWithAllAppsHash.items()]
    authWeight = [l for x,l in authListHash.items()]
    authWeight = [float(l)*50 for x,l in authWeight]
    print("Weights assigned")

    print("Map to layout (takes time)...")
    # Map to layout
    pos = nx.spring_layout(G, k=0.25, iterations=70, scale=10)
    print("size of graph: "+str(G.size()))
    plt.figure(figsize=(20, 20))

    print("Draw network..")
    # Draw network
    nx.draw_networkx_nodes(G, pos=pos, node_color="red", nodelist=listWithAllAppsHash.keys(), node_size=appWeight)
    nx.draw_networkx_nodes(G, pos=pos, node_color="blue", nodelist=authListHash.keys(), node_size=authWeight)
    nx.draw_networkx_edges(G, pos=pos)

    print("Add legend")
    # Add legend
    p = mlines.Line2D([],[],label="Author",color="blue")
    a = mlines.Line2D([],[],label="Application",color="red")
    plt.legend(handles=[p,a])

    try:
        print("Print graph")
        # Print graph list to output, and output image
        graphDictionaryFile.write(str(G.edges))
        plt.savefig("TopologicalAnalysis.jpg", dpi=40, pil_kwargs={'quality': 50})
    except:
        print("Reached exception when printing JPG")


    # Return graph to call function
    return G