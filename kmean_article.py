import collections
import math
import gensim as gs
import wikipedia
import string
import random
import util
import numpy as np
from spectrum import getRelativeCount

model = gs.models.Word2Vec.load('gensimModel')

listOfPageName = ['Sushi', 'Burrito', 'Thailand', 'google', 'Muslim', 'Islam', 'Pizza', 'South Korea', 'Andrew Ng', 'Barack Obama', 'Google']
pages = [util.getCleanWikiContent(names) for names in listOfPageName]
texts = [util.freqFilter(util.removeMeaningless(page.lower().split(' ')), 0.003, 1) for page in pages]
# texts = [getRelativeCount(name, listOfPageName, 4, 0.35) for name in listOfPageName]
# texts = [util.removeMeaningless(page.lower().split(' ')) for page in pages]
# print texts
# texts = util.truncatedList(texts, 0.5, 1)
# print texts
# print truncatedLists[0]

#List of list
resampledTexts = [util.updatedResample(text, 100) for text in texts]
countTexts = [collections.Counter(text) for text in resampledTexts]

# print collections.Counter(resampledTexts[0])

# text0 = list(set(resampledTexts[2]))
text0 = resampledTexts[2]
countText0 = countTexts[2]
text0_invocab = [word for word in text0 if word in model.vocab]
vecs = [model[word] for word in text0 if word in model.vocab]

#K-means
num_iter = 50
num_centroids = 20
min_cost = float('inf')
final_assignments = [-1 for i in range(len(vecs))]
for i in range(num_iter):

    #initialize cost of objective Function
    cost = 0

    #randomize centroids
    centroids = random.sample(vecs, num_centroids)

    preassignments = [0 for i in range(len(vecs))]
    assignments = [-1 for i in range(len(vecs))]

    # do until assignments coverge
    while assignments != preassignments:
        cost = 0
        preassignments = assignments

        #assigning centroids to each vector
        for i, vec in enumerate(vecs):
            norm = float('inf')
            assign = -1
            for index, centroid in enumerate(centroids):
                value = np.linalg.norm(vec - centroid)
                if value < norm:
                    assign = index
                    norm = value
            cost += norm
            assignments[i] = assign

        # recalculating the centroids
        mean_centroids = [np.array([0.0 for i in range(100)]) for j in range(num_centroids)]
        count_centroids = [0 for i in range(num_centroids)]
        for i in range(len(vecs)):
            mean_centroids[assignments[i]] += vecs[i]
            count_centroids[assignments[i]] += 1
        for i in range(num_centroids):
            if count_centroids[i] != 0:
                mean_centroids[i] = mean_centroids[i]/count_centroids[i]
        centroids = mean_centroids

    if cost < min_cost:
        final_assignments = assignments
        min_cost = cost


cluster = [[] for i in range(num_centroids)]
for i, word in enumerate(text0_invocab):
    index = final_assignments[i]
    cluster[index].append(word)

for index, centroid in enumerate(cluster):
    sum = 0
    print "+++++++++ ", index, " ++++++++++"
    for word in centroid:
        sum += countText0[word]
        print word
    if len(centroid) != 0:
        sum = sum/float(len(centroid))
    print sum

# print centroids

# texts = [page.lower().split(' ') for page in pages]
# print util.getCommonWordsFromList(texts, 0.6, 0)
