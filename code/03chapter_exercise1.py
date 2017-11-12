"""This file contains code for use with "Think Bayes",
by Allen B. Downey, available from greenteapress.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

Exercise from chapter 3 introduced the power law (1/x)^(-alpha),
but assumed that any train we saw came from one company of 
unknown size x.

Now assume that we are observing trains from an unknown number
of companies. What's the probability that we see N = 60

My answer as of right now is that this just reduces back to
the uniform case. 
"""

import thinkbayes
import thinkplot
import ipdb

from thinkbayes import Pmf, Percentile
from dice import Dice
from pprint import pprint


class OneCompanyTrain2(Dice):
    """Represents hypotheses about how many trains the company has."""

    def __init__(self, hypos, alpha=1.0):
        """Initializes the hypotheses with a power law distribution.

        hypos: sequence of hypotheses
        alpha: parameter of the power law prior
        """
        Pmf.__init__(self)
        self.alpha = alpha
        for hypo in hypos:
            self.Set(hypo, hypo**(-self.alpha))
        self.Normalize()

    def Likelihood(self, data, hypo):
        if hypo < data:
            return 0
        else:
            return hypo**(-self.alpha)

# Make a "size aware" version that also weights each probability
# estimate given the frequency of that size

class ManyCompanyTrain2(OneCompanyTrain2):

    def __init__(self, hypos, alpha=1.0):
        """The only difference from the OneCompany variant above
        is that the prior probability of each hypothesis is scaled
        by hypo/sum(hypos). This represents the likelihood that
        the train we see comes from a company with N trains.

        What this ends up reducing to, however, is a uniform prior,
        because sum(hypos) just ends up getting normalized away.

        hypos: sequence of hypotheses
        alpha: parameter of the power law prior
        """
        Pmf.__init__(self)
        self.alpha = alpha
        for hypo in hypos:
            self.Set(hypo, hypo**(-alpha) * hypo/sum(hypos))
        self.Normalize()


def MakePosterior(high, dataset, constructor):
    """Makes and updates a Suite.

    high: upper bound on the range of hypotheses
    dataset: observed data to use for the update
    constructor: function that makes a new suite

    Returns: posterior Suite
    """
    hypos = xrange(1, high+1)
    suite = constructor(hypos)
    suite.name = str(high)

    for data in dataset:
        suite.Update(data)

    return suite

def ComparePriors(constructors, labels, \
                  dataset = [60], largest_size = 1000):
    """Runs the likelihood of a train with number specified by
    dataset given a arbitrary number of priors.
    
    constructors = a list of anything that inherits from the Dice class
    labels = labels for these prior distributions
    dataset = the number of the train spotted
    largest_size = the assumed size of the largest train company out there
    """
    thinkplot.Clf()
    thinkplot.PrePlot(num=2)

    for constructor, label in zip(constructors, labels):
        suite = MakePosterior(largest_size, dataset, constructor)
        suite.name = label
        print "Expected Value for {}".format(suite.name)
        print"\t {}: {}".format(largest_size, suite.Mean())
        print("\t 90 percent Credibility Interval")
        interval = Percentile(suite,5), Percentile(suite,95)
        print '\t',  interval

        thinkplot.Pmf(suite)

    thinkplot.Save(root='one_many_firm_comparison',
                xlabel='Number of trains',
                ylabel='Probability')

if __name__ == '__main__':
    ComparePriors(constructors = [OneCompanyTrain2, ManyCompanyTrain2], \
                  labels = ['One Company Power Law', 'Many Company Power Law'])
