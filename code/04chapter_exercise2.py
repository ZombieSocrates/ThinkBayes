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
	ham_score and the user's good_karma both increase.

	* A user casts an upvote on a "bad" link: In this case, we want link 
	quality to go up but user reliability to go down. This means the link's 
	ham_score will go up, but the user's bad_karma will go up, too.

	* A user casts a downvote on a "good" link: We want the link quality to 
	go down and user reliability to go down as well. This means that the link's 
	spam_score and the user's bad_karma both increase.

	* A user casts a downvote on a "bad" link: We want to link quality to go 
	down but user reliability to go up. This means that the link's spam_score 
	will go up, but the user's good_karma goes up as a consequence.

So any upvote will increase link ham_score to some degree, and any downvote 
will increase link spam_score to some degree. To what degree, though? To a 
degree proportional to the to the reliability of the user. AKA the update made
to the link will be user_reliability * (ham_score OR spam_score).

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

	def get_reliability_score(self):
		'''The estimated user reliability would be the mean of the beta 
		distribution represented by its good_karma and bad_karma.
		'''
		return self.reliability_dist.Mean()

	def make_vote(self, reddit_link, vote_type):
		'''Given a link being voted on, and the type of vote, this method does 
		three things.

			1. Freezes user_reliability and link reliability before the vote.
			2. Updates the input link by calling the `process_vote` method.
			3. Updates the user's good_karma or bad_karma attribute depending 
			on whether the vote is "correct" or not.   
		'''
		if vote_type not in ["up","down"]:
			raise NotImplementedError
		user_coef = self.get_reliability_score()
		link_coef = reddit_link.get_quality_score()
		reddit_link.process_vote(user_coef, vote_type)
		false_positive = (vote_type == "up") & (link_coef < 0.5)
		false_negative = (vote_type == "down") & (link_coef >= 0.5)
		if false_positive or false_negative:
			self.reliability_dist.Update((0, link_coef * self.bad_karma))
		else:
			self.reliability_dist.Update((link_coef * self.good_karma, 0))
		self.good_karma = self.reliability_dist.alpha
		self.bad_karma = self.reliability_dist.beta

class RedditLink():

	def __init__(self, ham_score = 1, spam_score = 1):
		'''Might not be a way around this, but every time update is called
		we would need to reset the ham_score and spam_score attributes. This
		should be handled in the `process_vote` method.
		'''
		if ham_score * spam_score == 0:
			raise ValueError("Neither quality parameter can be set to zero")
		self.quality_dist = Beta(ham_score, spam_score)
		self.ham_score = self.quality_dist.alpha
		self.spam_score = self.quality_dist.beta

	def get_quality_score(self):
		'''The estimated link quality would be the mean of the beta 
		distribution represented by its ham_score and spam_score.
		'''
		return self.quality_dist.Mean()

	def process_vote(self, reliability_score, vote_type):
		'''Given a reliability_score from the user who made the vote and 
		the type of the vote, this will update the link's underlying 
		quality distribution and rebing the ham_score and spam_score 
		attributes.
		'''
		vote_map = {"up":(self.ham_score * reliability_score, 0),
			"down":(0, self.spam_score * reliability_score)}
		self.quality_dist.Update(vote_map[vote_type])
		self.ham_score = self.quality_dist.alpha
		self.spam_score = self.quality_dist.beta

def main():
	pass

if __name__ == "__main__":
	# PLEASE MOVE THIS TO THE MAIN METHOD WITH MORE TESTS
	a_quality_link = RedditLink(ham_score = 9, spam_score = 1)
	a_reputable_user = RedditUser(good_karma = 5, bad_karma = 1)
	ipdb.set_trace()
	print "a reputable user upvotes a quality link"
	print "both quality and reliability should go up"
	a_reputable_user.make_vote(a_quality_link, "up")
	ipdb.set_trace()
	print "a reputable user downvotes the quality link"
	print "both quality and reliability should go down"
	a_reputable_user.make_vote(a_quality_link, "down")
	ipdb.set_trace()






