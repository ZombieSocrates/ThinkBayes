"""This file contains code for use with "Think Bayes",
by Allen B. Downey, available from greenteapress.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html

Exercise from chapter 3 introduced the power law (1/x)^(-alpha),
but assumed that any train we saw came from one company of 
unknown size x.

Now assume that we are observing trains from an unknown number
of companies.
"""

import thinkbayes
import thinkplot
import ipdb

from thinkbayes import Pmf, Percentile
from dice import Dice


class Train(Dice):
    """Represents hypotheses about how many trains the company has."""


class Train2(Dice):
    """Represents hypotheses about how many trains the company has."""

    def __init__(self, hypos, alpha=1.0):
        """Initializes the hypotheses with a power law distribution.

        hypos: sequence of hypotheses
        alpha: parameter of the power law prior
        """
        Pmf.__init__(self)
        for hypo in hypos:
            self.Set(hypo, hypo**(-alpha))
        self.Normalize()


if __name__ == '__main__':
    sizes = [i for i in range(5,16)]
    company_sizes = Train2(sizes, alpha = 1.0)

    for x in sizes:
        print "Company with {} trains has probability of {}".format(x, company_sizes.Likelihood(5,x))
    

    ipdb.set_trace()
