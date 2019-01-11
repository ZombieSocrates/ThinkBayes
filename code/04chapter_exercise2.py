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

At its base, both users and links are modelled as beta distributions, where 
alpha represents a "goodness/quality" attribute and beta represents a 
"badness/spaminess" attribute. The mean of each object's beta distribution 
represents its estimated reliability (for a user) and its estimated quality
(for a link)

These alpha and beta parameters DON'T map directly to the number of up and
down votes given or received. Instead they condition the impact of each vote
cast according to the following four desired behaviors:

	* A user casts an upvote on a "good" link: In this case, we want link 
	quality to go up and user reliability to go up. This means that the link's 
	quality_score and the user's good_karma both increase.

	* A user casts an upvote on a "bad" link: In this case, we want link 
	quality to go up but user reliability to go down. This means the link's 
	quality_score will go up, but the user's bad_karma will go up, too.

	* A user casts a downvote on a "good" link: We want the link quality to 
	go down and user reliability to go down as well. This means that the link's 
	spam_score and the user's bad_karma both increase.

	* A user casts a downvote on a "bad" link: We want to link quality to go 
	down but user reliability to go up. This means that the link's spam_score 
	will go up, but the user's good_karma goes up as a consequence.

So any upvote will increase link quality_score to some degree, and any downvote 
will increase link spam_score to some degree. To what degree, though? To a 
degree proportional to the to the reliability of the user. AKA the update made
to the link will be user_reliability * (quality_score OR spam_score).

The impact on the user is a little less direct, depending not only on the type 
of vote but also on whether the link is "good" or "bad." For the time being, I
will consider any link with estimated quality >= 0.5 "good".

	* Correct votes (up on "good", down on "bad") increase the user's 
	good_karma proportional to the quality of the link
	* Incorrect votes (down on "good", up on "bad") increase the user's 
	bad_karma proportional to the quality of the link 

TKTK 1: Need to actually test the four scenarios in the main method
TKTK 2: Could the we add user good_karma and bad_karma values to links
and add link quality and spam scores to the users in order to make these 
updates, instead of just multiplying.
'''       




class RedditUser():

	def __init__(self, good_karma = 1, bad_karma = 1):
		'''Create each user's underlying beta distribution, paramaterized by 
		their good_karma and bad_karma score. Might not be a way around this, 
		but every time update is called we would need to reset the good_karma 
		and bad_karma attributes.
		'''
		if good_karma * bad_karma == 0:
			raise ValueError("Neither user parameter can be set to zero")
		self.reliability_dist = Beta(good_karma, bad_karma)
		self.good_karma = self.reliability_dist.alpha
		self.bad_karma = self.reliability_dist.beta

	def get_user_reliability(self):
		'''The estimated user reliability would be the mean of the beta 
		distribution represented by its good_karma and bad_karma
		'''
		return self.reliability_dist.Mean()

	def make_vote_and_update(self, reddit_link, vote_type):
		'''What link is this person voting on and is it an upvote or a down 
		vote? 

		An upvote will always increase the link's plus score, while a downvote
		will always add to the spam score. The degree to which this happens is
		weighted by the user's reliability score. 

		NO...STUPID...MAKE BASICALLY ALL OF THIS STUFF PART OF THE LINK OBJECT
		V    V     V    V    V   
		As it stands now, this method changes the quality distribution of the 
		RedditLink object. The `update_user_from_vote` method handles all changes  
		'''
		if vote_type not in ["up","down"]:
			raise NotImplementedError
		user_factor = self.get_user_reliability()
		vote_map = {"up":(reddit_link.quality_score * user_factor, 0),
			"down":(0, reddit_link.spam_score * user_factor)}
		reddit_link.quality_dist.Update(vote_map[vote_type])
		reddit_link.quality_score = reddit_link.quality_dist.alpha
		reddit_link.spam_score = reddit_link.quality_dist.beta


class RedditLink():

	def __init__(self, quality_score = 1, spam_score = 1):
		'''Might not be a way around this, but every time update is called
		we would need to reset the quality_score and spam_score attribute. This
		should be handled in the `update_from_vote` method.
		'''
		if quality_score * spam_score == 0:
			raise ValueError("Neither quality parameter can be set to zero")
		self.quality_dist = Beta(quality_score, spam_score)
		self.quality_score = self.quality_dist.alpha
		self.spam_score = self.quality_dist.beta

	def get_link_quality(self):
		'''The estimated link quality would be the mean of the beta 
		distribution represented by its quality_score and spam_score.
		'''
		return self.quality_dist.Mean()

	def update_link_from_vote(self, reddit_user, vote_type):
		'''What user is voting on this, and is it an upvote or a down vote? 
		Still need to think about how the respective updates will happen.
		'''
		print "WHEE"

if __name__ == "__main__":
	a_quality_link = RedditLink(quality_score = 9, spam_score = 1)
	a_reputable_user = RedditUser(good_karma = 5, bad_karma = 1)
	ipdb.set_trace()






