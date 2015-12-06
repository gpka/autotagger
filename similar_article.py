
import collections
import math
import gensim as gs
import wikipedia
import string
import random
import util
import numpy as np

def cosine(c1, c2):
	return np.dot(c1, c2)/(np.linalg.norm(c1) * np.linalg.norm(c2))

def one_way_similar(kmeans1, kmeans2):
	centroids1, weight1 = kmeans1[0], kmeans1[1]
	centroids2, weight2 = kmeans2[0], kmeans2[1]
	dist_list = []
	for index1, centroid1 in enumerate(centroids1):
		if weight1[index1] == 0 or np.linalg.norm(centroid1) == 0: continue
		dist_list.append(max(weight1[index1]*cosine(centroid1, centroid2) \
						for index2, centroid2 in enumerate(centroids2) if weight2[index2] != 0 and np.linalg.norm(centroid2)))
	return sum(dist_list)

def similar(kmeans1, kmeans2):
	return np.array([one_way_similar(kmeans1, kmeans2), one_way_similar(kmeans2, kmeans1)])

while 1:
	title1 = raw_input('Insert the first title:')
	title2 = raw_input('Insert the second title:')
	if len(title1) == 0 or len(title2) == 0: break
	result = similar(util.k_means(title1), util.k_means(title2))
	print "Similarity between two articles is (%f, %f)" % (result[0], result[1])
