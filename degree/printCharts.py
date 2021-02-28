from pylab import *
from scipy.stats import stats
import powerlaw # Power laws are probability distributions with the form:p(x)∝x−α


from degree.histogram import generateDegreeHistogram


def printHistograms(G, auth, app):
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
    plt.loglog(degrees_2, degree_freq_auth, 'ro', markerfacecolor='none')
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.legend(title="Degree distribution of Authors (# of reviews)", fontsize=10, title_fontsize=15)
    plt.savefig("degree/histogram_author.jpg", dpi=200, pil_kwargs={'quality': 100})
    plt.close()

    jaime = sorted([d for n, d in G.degree() if n in app])
    plot6 = plt.figure(figsize=(12, 8))
    degree_sequence = sorted([d for d in degrees], reverse=True)  # used for degree distribution and powerlaw test
    fit = powerlaw.Fit(jaime, xmin=1)
    fig2 = fit.plot_pdf(color='b', linewidth=2)
    fit.power_law.plot_pdf(color='g', linestyle='--', ax=fig2)
    plt.legend(title="Power-law fit Apps", fontsize=10, title_fontsize=15)
    plt.xlabel('Degree(k)')
    plt.ylabel('Probability p(k)')
    plt.savefig("degree/power_app.jpg", dpi=200, pil_kwargs={'quality': 100})
    plt.close()

    jaime = sorted([d for n, d in G.degree() if n in auth])
    plot7 = plt.figure(figsize=(12, 8))
    degree_sequence = sorted([d for d in degrees], reverse=True)  # used for degree distribution and powerlaw test
    fit_u = powerlaw.Fit(jaime, xmin=1)
    fig2 = fit.plot_pdf(color='b', linewidth=2)
    fit_u.power_law.plot_pdf(color='g', linestyle='--', ax=fig2)
    plt.legend(title="Power-law fit Authors", fontsize=10, title_fontsize=15)
    plt.xlabel('Degree(k)')
    plt.ylabel('Probability p(k)')
    plt.savefig("degree/power_auth.jpg", dpi=200, pil_kwargs={'quality': 100})
    plt.close()


    plot8 = plt.figure(figsize=(12, 8))
    fit_u.distribution_compare('power_law', 'lognormal')
    fig4 = fit_u.plot_ccdf(linewidth=3, color='black')
    fit_u.power_law.plot_ccdf(ax=fig4, color='r', linestyle='--',label='Power-law')  # powerlaw
    fit_u.lognormal.plot_ccdf(ax=fig4, color='g', linestyle='--',label='log normal')  # lognormal
    fit_u.stretched_exponential.plot_ccdf(ax=fig4, color='b', linestyle='--',label='Exponential')  # stretched_exponential
    plt.xlabel('Degree(k)')
    plt.ylabel('Probability p(k)')
#    plt.legend(plot5[:3], ['Power-law', 'log normal', 'Exponential'])
    plt.savefig("degree/power3.jpg", dpi=200, pil_kwargs={'quality': 100})

