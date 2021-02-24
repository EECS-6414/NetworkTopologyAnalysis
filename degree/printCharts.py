from pylab import *
from scipy.stats import stats
import powerlaw # Power laws are probability distributions with the form:p(x)∝x−α


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
    plt.loglog(degrees_2, degree_freq_auth, 'ro', markerfacecolor='none')
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.legend(title="Degree distribution of Authors (# of reviews)", fontsize=10, title_fontsize=15)
    plt.savefig("degree/histogram_author.jpg", dpi=200, pil_kwargs={'quality': 100})
    plt.close()

    m, b, r_value, p_value, std_err = stats.linregress(degrees, degree_freq_app)
    print("slope: "+str(m))
    print("r-squared: "+str(r_value**2))
    print("intercept:"+ str(b))
    plot3 = plt.figure(figsize=(12, 8))
    plt.plot(degrees, degree_freq_app, 'o',color = 'r')
    abline_values = [m * i + b for i in degrees]
    plt.plot(degrees, abline_values)
    title = "Power-law distribution with -α = "+str(-1*m)
    plt.legend(title=title, fontsize=10, title_fontsize=15)
    plt.savefig("degree/power.jpg", dpi=200, pil_kwargs={'quality': 100})

    degree_sequence = sorted([d for n, d in G.degree()], reverse=True)  # used for degree distribution and powerlaw test
    plt.close()
    fit = powerlaw.Fit(degree_sequence)
    plot4 = fit.plot_pdf(color='b', linewidth=2)
    fit.power_law.plot_pdf(color='g', linestyle='--', ax=plot4)
    plt.legend(title="Power-law fit", fontsize=10, title_fontsize=15)
    plt.xlabel('Degree(k)')
    plt.ylabel('Probability p(k)')
    plt.savefig("degree/power2.jpg", dpi=200, pil_kwargs={'quality': 100})
    # compare
    # where R is the likelihood ratio between the two candidate distributions. This number will be positive if the data is more likely in the first distribution, but you should also check p < 0.05
    R, p = fit.distribution_compare('power_law', 'exponential', normalized_ratio=True)
    print(R, p)
    plt.close()

    plot5 = plt.figure(figsize=(10, 6))
    fit.distribution_compare('power_law', 'log normal')
    fig4 = fit.plot_ccdf(linewidth=3, color='black')
    fit.power_law.plot_ccdf(ax=fig4, color='r', linestyle='--',label='Power-law')  # powerlaw
    fit.lognormal.plot_ccdf(ax=fig4, color='g', linestyle='--',label='log normal')  # lognormal
    fit.stretched_exponential.plot_ccdf(ax=fig4, color='b', linestyle='--',label='Exponential')  # stretched_exponential
    plt.xlabel('Degree(k)')
    plt.ylabel('Probability p(k)')
    plt.legend(plot5[:3], ['Power-law', 'log normal', 'Exponential'])
    plt.savefig("degree/power3.jpg", dpi=200, pil_kwargs={'quality': 100})

