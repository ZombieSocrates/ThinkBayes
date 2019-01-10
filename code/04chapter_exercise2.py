# import thinkbayes
# import thinkplot

import ipdb

from random import uniform
from thinkbayes import Beta

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

Model both users and links as beta distributions. I originally thought that in 
the case of links, the parameters alpha and beta could correspond rather 
nicely to number of upvotes and number of downvotes For users, you could have 
something similar with "correct votes" vs "incorrect votes." HOWEVER, the whole 
gist here is that each vote shouldn't have an equal impact..


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

	def __init__(self, good_karma = 1, bad_karma = 1):
		'''Might not be a way around this, but every time update is called
		we would need to reset the good_karma and bad_karma attribute. This
		should be handled in the `update_from_vote` method.
		'''
		if good_karma * bad_karma == 0:
			raise ValueError("Neither user parameter can be set to zero")
		self.reliability_dist = thinkbayes.Beta(good_karma, bad_karma)
		self.good_karma = self.reliability_dist.alpha
		self.bad_karma = self.reliability_dist.beta

	def get_user_reliability(self):
		'''The estimated user reliability would be the mean of the beta 
		distribution represented by its good_karma and bad_karma
		'''
		return self.reliability_dist.Mean()


	def make_vote(self, reddit_link, vote_type):
		'''What link is this person voting on and is it an upvote or a down 
		vote? Still need to think about how the respective updates will happen.
		'''
		pass


class RedditLink():

	def __init__(self, plus_score = 1, spam_score = 1):
		'''Might not be a way around this, but every time update is called
		we would need to reset the plus_score and spam_score attribute. This
		should be handled in the `update_from_vote` method.
		'''
		if plus_score * spam_score == 0:
			raise ValueError("Neither quality parameter can be set to zero")
		self.quality_dist = Beta(plus_score, spam_score)
		self.plus_score = self.quality_dist.alpha
		self.spam_score = self.quality_dist.beta

	def get_link_quality(self):
		'''The estimated link quality would be the mean of the beta 
		distribution represented by its plus_score and spam_score.
		'''
		return self.quality_dist.Mean()

	def update_from_vote(self, reddit_user, vote_type):
		'''What user is voting on this, and is it an upvote or a down vote? 
		Still need to think about how the respective updates will happen.
		'''
		pass


if __name__ == "__main__":
	a_link = RedditLink()
	ipdb.set_trace()





