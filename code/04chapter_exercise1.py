import thinkbayes
import thinkplot

from random import uniform
from collections import Counter

import ipdb


'''
Suppose that instead of observing coin tosses directly, you measure the outcome 
using an instrument that is not always correct. Specifically, suppose there is a 
probability y that an actual heads is reported as tails, or actual tails reported 
as heads. Write a class that estimates the bias of a coin given a series of 
outcomes and the value of y.

How does the spread of the posterior distribution depend on y?


A lot of this I was basically able to copy over from `euro.py`. The main thing
that I changed was the RunUpdate method, so that it will make errors according
to whatever value of y I set
'''

class Euro(thinkbayes.Suite):
    """Represents hypotheses about the probability of heads."""

    def Likelihood(self, data, hypo):
        """Computes the likelihood of the data under the hypothesis.

        hypo: integer value of x, the probability of heads (0-100)
        data: string 'H' or 'T'
        """
        x = hypo / 100.0
        if data == 'H':
            return x
        else:
            return 1-x

def UniformPrior():
    """Makes a Suite with a uniform prior."""
    suite = Euro(xrange(0, 101))
    return suite


def TrianglePrior():
    """Makes a Suite with a triangular prior."""
    suite = Euro()
    for x in range(0, 51):
        suite.Set(x, x)
    for x in range(51, 101):
        suite.Set(x, 100-x) 
    suite.Normalize()
    return suite


def RunUpdate(suite, error_prob, heads=140, tails=110):
    """Updates the Suite with the given number of heads and tails.

    suite: Suite object
    heads: int
    tails: int
    """
    dataset = 'H' * heads + 'T' * tails

    for data in dataset:
    	err = uniform(0,1) <= error_prob
    	if (err and data == 'H') or (not err and data =='T'):
        	suite.Update('T')
        else:
        	suite.Update('H')


def Summarize(suite):
    """Prints summary statistics for the suite."""
    print '\tProbability of 50', suite.Prob(50)
    print '\tMLE', suite.MaximumLikelihood()
    print '\tMean', suite.Mean()
    print '\tMedian', thinkbayes.Percentile(suite, 50) 
    print '\t90% CI', thinkbayes.CredibleInterval(suite, 90)
    print '\n'


def PlotSuites(suites, root):
    """Plots two suites.

    suite1, suite2: Suite objects
    root: string filename to write
    """
    thinkplot.Clf()
    thinkplot.PrePlot(len(suites))
    thinkplot.Pmfs(suites)

    thinkplot.Save(root=root,
                   xlabel='x',
                   ylabel='Probability',
                   formats=['pdf', 'eps'])

def main(error_prob, plot_priors = False):
    # make the priors
    suite1 = UniformPrior()
    suite1.name = 'uniform'

    suite2 = TrianglePrior()
    suite2.name = 'triangle'

    if plot_priors:
	    # plot the priors
    	PlotSuites([suite1, suite2], 'prior_dists_{}'.format(error_prob))

    # update
    RunUpdate(suite1, error_prob)
    print 'Summary for {}'.format(suite1.name)
    Summarize(suite1)

    RunUpdate(suite2, error_prob)
    print 'Summary for {}'.format(suite2.name)
    Summarize(suite2)

    # plot the posteriors
    # PlotSuites([suite1], 'uniform')
    PlotSuites([suite1, suite2], 'uniform_triangular_{}'.format(error_prob))
    print '-------------------\n'


if __name__ == '__main__':
	list_of_errs = [0, 0.05, 0.15, 0.45, 0.85]
	for err in list_of_errs:
		print "Assumed Measurement Error: {}".format(err)
		main(err)