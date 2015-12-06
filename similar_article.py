
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
	centroids1, weight1 = kmeans1[0], kmeans1[1]
	centroids2 = kmeans2[0]
	dist_list = []
	for index, centroid1 in enumerate(centroids1):
		dist_list.append(max(weight1[index]/(np.linalg.norm(centroid1 - centroid2) + 1) for centroid2 in centroids2))

	return sum(dist_list)

def similar(kmeans1, kmeans2):
	return np.array([one_way_similar(kmeans1, kmeans2), one_way_similar(kmeans2, kmeans1)])

def average_similar(kmeans1, kmeans2, iteration):
	return sum(similar(kmeans1, kmeans2) for i in range(iteration))/iteration

text_1 = 'Microsoft'
text_2 = 'Google'
iterate = 10
kmean_1 = util.k_means(text_1)
kmean_2 = util.k_means(text_2)
print text_1,',', text_2, iterate
print average_similar(kmean_1, kmean_2, iterate)

