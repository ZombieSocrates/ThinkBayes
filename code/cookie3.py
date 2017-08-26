"""This file contains code for use with "Think Bayes",
by Allen B. Downey, available from greenteapress.com

Copyright 2012 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""

from thinkbayes import Pmf

class Bowl(object):
    '''A separate object that keeps track of how many
    cookies of each type are in a bowl. All it basically
    does is produce likelihoods and update those upon
    selection
    '''
    def __init__(self, n_vanilla, n_chocolate):
        self.vanilla = n_vanilla
        self.chocolate = n_chocolate

    def get_bowl_likelihood(self):
        '''Added an edge case to account for the possibility of
        someone trying to select more than V + C cookies from
        the bowl
        '''
        total = self.vanilla + self.chocolate
        if total == 0:
            return dict(vanilla=0.0, chocolate = 0.0)
        v_prob = float(self.vanilla * 1.0/total)
        c_prob = float(self.chocolate * 1.0/total)
        return dict(vanilla=v_prob, chocolate = c_prob)

    def update_bowl_likelihood(self, cookie_string):
        '''Edge case added to avoid the possibility of
        negative cookies 
        '''
        if cookie_string not in ['vanilla','chocolate']:
            raise NotImplementedError
        elif cookie_string == 'vanilla':
            self.vanilla = max(self.vanilla - 1, 0)
        else:
            self.chocolate = max(self.chocolate -1, 0)
        return self.get_bowl_likelihood()


class Cookie(Pmf):
    """A map from string bowl ID to probablity."""

    # Pmf starts out with two bowls of 40 cookies each,
    # and populates the mixes dictionary with the initial
    # bowl likelihoods
    B1 = Bowl(n_vanilla=30, n_chocolate=10)
    B2 = Bowl(n_vanilla=20, n_chocolate=20)

    mixes = {
        'Bowl 1':B1.get_bowl_likelihood(),
        'Bowl 2':B2.get_bowl_likelihood(),
        }

    def __init__(self, hypos):
        """Initialize self.

        hypos: sequence of string bowl IDs
        """
        Pmf.__init__(self)
        for hypo in hypos:
            self.Set(hypo, 1)
        self.Normalize()

    def Update(self, data):
        """Updates the PMF with new data.

        data: string cookie type
        """
        for hypo in self.Values():
            like = self.Likelihood(data, hypo)
            self.Mult(hypo, like)
        self.Normalize()

    def Likelihood(self, data, hypo):
        """The likelihood of the data under the hypothesis.

        data: string cookie type
        hypo: string bowl ID
        """
        mix = self.mixes[hypo]
        like = mix[data]
        return like


def main():
    hypos = ['Bowl 1', 'Bowl 2']

    pmf = Cookie(hypos)

    dataset = ['vanilla','chocolate','vanilla']
    replacement = True
    for data in dataset:
        # print 'Bowl 1: Chocolate {}, Vanilla {}'.format(pmf.B1.chocolate, pmf.B1.vanilla)
        # print 'Bowl 2: Chocolate {}, Vanilla {}'.format(pmf.B2.chocolate, pmf.B2.vanilla)
        pmf.Update(data)
        # If sampling with replacement, update the mixes dictionary after each draw
        if replacement:
            pmf.mixes['Bowl 1'] = pmf.B1.update_bowl_likelihood(data)
            pmf.mixes['Bowl 2'] = pmf.B2.update_bowl_likelihood(data)
            # print 'removed {}\n'.format(data)


    for hypo, prob in pmf.Items():
        print hypo, prob


if __name__ == '__main__':
    # import ipdb
    # ipdb.set_trace()
    main()