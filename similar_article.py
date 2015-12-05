
import collections
import math
import gensim as gs
import wikipedia
import string
import random
import util
import numpy as np


# Input: 
# kmean = (centroids, weight) 
# where centroids = array of numpy 
# and weight = list of number
# Output:
# sum of closest distance for each cluster
def one_way_similar(kmeans1, kmeans2):
	centroids1, centroids2 = kmeans1[0], kmeans2[0]
	dist_list = []
	for centroid1 in centroids1:
		dist_list.append(min(np.linalg.norm(centroid1 - centroid2) for centroid2 in centroids2))

	return sum(dist_list)

def similar(kmeans1, kmeans2):
	return (one_way_similar(kmeans1, kmeans2), one_way_similar(kmeans2, kmeans1))

kmean_1 = util.k_means('Thailand')
kmean_2 = util.k_means('Japan')
print similar(kmean_1, kmean_2)

