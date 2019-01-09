import thinkbayes
import thinkplot

import ipdb

'''
Redditors post links to online content and other web pages. Other redditors 
vote on the links, giving an "upvote" to high-quality links and a "downvote" 
to links that are bad or irrelevant. A problem is that some redditors are 
more reliable than others, and Reddit does not take this into account.

The challenge is to devise a system so that when a redditor casts a vote, the 
estimated quality of the link is updated in accordance with the reliability of 
the redditor, and the estimated reliability of the redditor is updated in 
accordance with the quality of the link.

One approach is to model the quality of the link as the probability of 
garnering an upvote, and to model the reliability of the redditor as the 
probability of correctly giving an upvote to a high-quality item.

Write class definitions for redditors and links and an update function that 
updates both objects whenever a redditor casts a vote.

MY ANSWER: IN PROGRESS

IDEA SO FAR:

Model both users and links as beta distributions.

At least in the case of links, the parameters alpha and beta
could correspond rather nicely to number of upvotes and number of downvotes

For users, you could have something similar with "correct votes" vs
"incorrect votes."


I had this half-formed idea of being able to update each object by 
mutual addition. That is when a user with a,b votes on a link with c,d,
the new "reliability parameters" would be a + c, b + d. The only trouble
here is that ...
	we wouldn't want to add a high amount of unreliability to an
valid article because a junky user votes on it
	we could have instances where people get caught in a = b and c = d
scenarios

There's some kind of confusion matrix to take into account here,
and I need to think about how a score would ideally change if

	* A highly reliable user correctly votes (up or down) on an article
	* A highly unreliable user correctly votes on an article
	* A highly reliable user incorrectly votes
	* A highly unreliable user incorrectly votes

'''       




class RedditUser():

	def __init__(self):
		pass

	def update(self):
		pass


class RedditLink():

	def __init__(self):
		self.quality_dist = thinkbayes.Beta()
		self.upvotes = self.quality_dist.alpha
		self.downvotes = self.quality_dist.beta


if __name__ == "__main__":
	a_link = RedditLink()
	# At this point, you need to modify the
	# quality dist attribute to simulate the act
	# of upvoting and downvoting
	ipdb.set_trace()





