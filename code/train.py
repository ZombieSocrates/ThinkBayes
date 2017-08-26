"""This file contains code for use with "Think Bayes",
by Allen B. Downey, available from greenteapress.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from dice import Dice
import thinkplot


class Train(Dice):
    """Represents hypotheses about how many trains the company has.

    The likelihood function for the train problem is the same as
    for the Dice problem.
    """


def main():
    uppers = [500,1000,2000]
    for upper in uppers:
        hypos = xrange(1, upper + 1)
        suite = Train(hypos)

        data_vals = [60,30,90]
        for i, data in enumerate(data_vals):
            suite.Update(data)
            print "Prior from 1 to {}, evidence {}".format(upper, data_vals[:i+1])
            print "Mean of posterior: {}".format(suite.Mean())

    # thinkplot.PrePlot(1)
    # thinkplot.Pmf(suite)
    # thinkplot.Save(root='train1',
    #                xlabel='Number of trains',
    #                ylabel='Probability',
    #                formats=['pdf', 'eps'])


if __name__ == '__main__':
    main()
