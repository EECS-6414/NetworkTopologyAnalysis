import pandas
from pylab import *
import networkx as nx
import pandas as pd
import matplotlib.lines as mlines
from operator import itemgetter
from fileNames import files
from statistics import mean

def timeit(func):
    """
    Decorator for measuring function's running time.
    """
    def measure_time(*args, **kw):
        start_time = time.time()
        result = func(*args, **kw)
        print("Processing time of %s(): %.2f seconds."
              % (func.__qualname__, time.time() - start_time))
        return result

    return measure_time

@timeit
def TNAfunc(path, names):
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
            appList.append(splitVal[j].strip())

    for i in range(appNamesFile['App'].count()+1):
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
    count=0
    for i in range(dataset['Author'].count()):
        aVal1 = dataset['Author'][i]
        aVal2 = dataset['App'][i]
        aVal3 = dataset['App ID'][i]
        aVal4 = dataset['Total'][i]

        parts = aVal2.split(";")
        listAux = []
        for p in parts:
            listAux.append(p)
        listAux = set(listAux)
        if len(parts) != len(listAux):
            count+=1
        else:
            authListHash[aVal1] = aVal2, aVal3, aVal4
    print("Repeated names of authors: "+str(count))


    print("getting sentiment...")
    authListHash2 = {}

    # Here we add the sentiment besides the app name with the separator "!?$"
    for index, item in enumerate(names):
        print("processing index (out of 500): "+str(index))
        try:
            filePath = pandas.read_csv(str(path+"/"+item))
        except:
            print("couldn't read file")
        appSingleName = item[31:len(item)-4]
        for i in range(len(filePath)):
            if authListHash.get(filePath['Author'][i])!=None:
                try:
                    splitId = authListHash[filePath['Author'][i]][1].split(";")
                    splitApp = authListHash[filePath['Author'][i]][0].split(";")
                    idValue = authListHash[filePath['Author'][i]][1]
                    idFrequency = authListHash[filePath['Author'][i]][2]
                    for j in range(len(splitId)):
                        if splitId[j] == appSingleName:
                            sentiment = 'k'
                            if filePath['sentiment'][i]=='negative':
                                sentiment = 'r'
                            elif filePath['sentiment'][i]=='positive':
                                sentiment = 'b'
                            splitApp[j] = splitApp[j]+"!?$"+sentiment
                            authListHash2[filePath['Author'][i]] = splitApp[0:len(splitApp)], idValue, idFrequency
                except:
                    print("Error")
    print("number of authors: "+str(len(authListHash2)))

    # Create and name graph
    G = nx.Graph()
    G.name = "Topological Network Analysis"

    # Add author list and apps list
    G.add_nodes_from(listWithAllAppsHash.keys())
    G.add_nodes_from(authListHash2.keys())

    # Add edge between every author and every app they commented on
    print("building network (9 min)...")
    for key, value in authListHash2.items():
        for k, v in listWithAllAppsHash.items():
            if str(k) in str(value[0]):
                color = 'k'
                for n in range(len(value[0])):
                    if '!?$' in value[0][n] and str(k) in value[0][n]:
                        try:
                            partsWeigh = value[0][n].split("!?$")
                            color = partsWeigh[1]
                        except:
                            color = 'k';
                G.add_edge(key, k, color=color)
                listWithAllAppsHash[k] += 1


    # Print statistical information
    print(nx.info(G))
    topologyStatisticsFile.write(str(nx.info(G))+"\n")
    density = nx.density(G)
    print("Network density:", density)
    topologyStatisticsFile.write("Network density: "+str(density))
    degree_dict = dict(G.degree(G.nodes()))
    print("Extracting degree...")
    degreeOfApp = {}
    degreeOfAuthors = {}
    for k, v in degree_dict.items():
        if k in listWithAllAppsHash:
            degreeOfApp[k] = v
        else:
            degreeOfAuthors[k] = v
    degreeOfApp = sorted(degreeOfApp.items(), key=lambda x: x[1], reverse=True)
    degreeOfAuthors = sorted(degreeOfAuthors.items(), key=lambda x: x[1], reverse=True)
    appHighestDegree = str(list(degreeOfApp[0])[0]) + " - " + str(list(degreeOfApp[0])[1])
    authorHighestDegree = str(list(degreeOfAuthors[0])[0]) + " - " + str(list(degreeOfAuthors[0])[1])
    topologyStatisticsFile.write(appHighestDegree)
    topologyStatisticsFile.write(authorHighestDegree)
    print("average degree...")
    count = 0
    for v in degreeOfApp:
        count += v[1]
    topologyStatisticsFile.write("\nNode degree av. APP: "+str(count/len(degreeOfApp)))
    count = 0
    for v in degreeOfAuthors:
        count += v[1]
    topologyStatisticsFile.write("\nNode degree av. Author: "+str(count/len(degreeOfAuthors)))
    topologyStatisticsFile.write("\nTop 10 Authors:\n")
    for v in range(10):
        topologyStatisticsFile.write(str(degreeOfAuthors[v])+"\n")

    nx.set_node_attributes(G, degree_dict, 'degree')
    sorted_degree = sorted(degree_dict.items(), key=itemgetter(1), reverse=True)
    print("Top 5 nodes by degree:")
    topologyStatisticsFile.write("\nTop 10 Apps:\n")
    for d in sorted_degree[:10]:
        print(d)
        topologyStatisticsFile.write(str(d)+"\n")

    # Determine node size
    authWeight = []
    appWeight = [float(l)*50 for x,l in listWithAllAppsHash.items()]
    for i in authListHash2.items():
        authWeight.append(float(i[1][2])*50)
    print("Weights assigned")
    colors = nx.get_edge_attributes(G, 'color').values()

    print("Graph completed!")

    # print("Map to layout (takes time)...")
    # # Map to layout
    # pos = nx.spring_layout(G, k=0.25, iterations=70, scale=10)
    # print("size of graph: "+str(G.size()))
    # plt.figure(figsize=(20, 20))
    #
    # print("Draw network..")
    # # Draw network
    # nx.draw_networkx_nodes(G, pos=pos, node_color="red", nodelist=listWithAllAppsHash.keys(), node_size=appWeight)
    # nx.draw_networkx_nodes(G, pos=pos, node_color="blue", nodelist=authListHash2.keys(), node_size=authWeight)
    # nx.draw_networkx_edges(G, pos=pos,edge_color=colors)
    #
    # print("Add legend")
    # # Add legend
    # p = mlines.Line2D([],[],label="Author",color="blue")
    # a = mlines.Line2D([],[],label="Application",color="red")
    # plt.legend(handles=[p,a])
    #
    # try:
    #     print("Print graph")
    #     # Print graph list to output, and output image
    #     graphDictionaryFile.write(str(G.edges))
    #     plt.savefig("TopologicalAnalysis.jpg", dpi=200, pil_kwargs={'quality': 50})
    # except:
    #     print("Reached exception when printing JPG")


    # Return graph to call function
    return G