from __future__ import division
# Meant to convert comment counts to zero-mean, unit variance within
# each blog so that we can get a better sense of the effect of 
# word count on number of comments and control for inter-blog variability

import cPickle as pickle 
import numpy as np 
import scipy.stats as stats

# Load the pickled dictionary file
with open("blog_dict.pck","rb") as f:
	all_posts = pickle.load(f)

normal_dict = dict.fromkeys(all_posts,[])

for blog in all_posts:
	print "Now processing:\n", all_posts[blog]
	comment_counts = [x[1] for x in all_posts[blog]]
	print "\ncomment_counts=", comment_counts
	avg = np.mean(comment_counts)
	print "\navg = ", avg
	if avg != 0:
		print "\nNon-zero mean!"
		variance = 1
		print "\nvariance = ", variance
		for index, count in enumerate(comment_counts):
			#normal_dict[blog].append((all_posts[blog][index][0], 
				#(count - avg)/variance))
			normal_dict[blog].append((all_posts[blog][index][0], 
				count/np.max(comment_counts)))
		print "\nNormalized Entry = \n", normal_dict[blog]
	else:
		del normal_dict[blog]

with open("normalized_blog_dict.pck","wb") as out:
	pickle.dump(normal_dict, out)



