from pylab import *

from degree.histogram import generateDegreeHistogram


def printHistograms(G):
    print("Creating histogram...")

    degree_freq_app = generateDegreeHistogram(G, "app")
    degrees = range(len(degree_freq_app))
    plot1 = plt.figure(figsize=(12, 8))
    plt.loglog(degrees, degree_freq_app, 'ro', markerfacecolor='none')
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.legend(title="Degree distribution of Apps", fontsize=10, title_fontsize=15)
    plt.savefig("degree/histogram_app.jpg", dpi=200, pil_kwargs={'quality': 100})
    plt.close()

    degree_freq_auth = generateDegreeHistogram(G, "author")
    degrees_2 = range(len(degree_freq_auth))
    plot2 = plt.figure(figsize=(12, 8))
    # print("length of author:"+str(degrees_2))
    # print("value author 1:"+str(degree_freq_auth.pop(0)))
    # print("value author 2:"+str(degree_freq_auth.pop(1)))
    # print("value author 3:"+str(degree_freq_auth.pop(2)))
    # print("value author max:"+str(degree_freq_auth.pop(len(degree_freq_auth)-1)))
    plt.loglog(degrees_2, degree_freq_auth, 'ro', markerfacecolor='none')
    # print(max(degrees_2))
    # plt.xlim(0, max(degrees_2))
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.legend(title="Degree distribution of Authors (# of reviews)", fontsize=10, title_fontsize=15)
    plt.savefig("degree/histogram_author.jpg", dpi=200, pil_kwargs={'quality': 100})