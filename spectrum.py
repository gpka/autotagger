import math, collections
import wikipedia
from util import getWordCountWiki

# Given two article, return a word spectrum. Input must be a Counter.
def getPairUniqueness(article1, article2, smooth=1, returntype=collections.Counter):
    result = returntype()
    if article1==article2:
        return result
    for w in article1:
        result[w] = 1
    for w in article2:
        result[w] = 1
    for w in result:
        result[w] = float(article1[w] + smooth) / float(article2[w] + smooth)
    return result

def getLogPairUniqueness(article1, article2, smooth=1, returntype=collections.Counter):
    result = returntype()
    if article1==article2:
        return result
    for w in article1:
        result[w] = 1
    for w in article2:
        result[w] = 1
    for w in result:
        result[w] = math.log(float(article1[w] + smooth) / float(article2[w] + smooth))
    return result

#####################################################################################
# Compare two article and rank other words in the article onto a spectrum
# This functions is pretty magical. Can be very useful ! ! !

def getWikiPairUniqueness(title1, title2, smooth=1, returntype=collections.Counter):
    return getLogPairUniqueness(getWordCountWiki(title1), getWordCountWiki(title2), smooth, returntype)

def normalizedCompare(title1, title2, smooth=1, returntype=collections.Counter):
    if title1==title2:
        return returntype()
    maxi, mini = float('-inf'), float('inf')
    result = getWikiPairUniqueness(title1, title2, smooth, returntype)
    for words in result:
        maxi = max(maxi, result[words])
        mini = min(mini, result[words])
    for words in result:
        result[words] = 2 * float(result[words] - mini) / (maxi - mini) - 1
    return result

# OddOneOut model
<<<<<<< HEAD
def oddOneOut(article1, article2, article3):
    raise Exception("Not implemented")


def getRelativeLogUniqueness(article, key, smooth=1, returntype=collections.Counter):
    result = returntype()
    for w in article:
        result[w] = (math.log(float(article[w] + smooth)) - math.log(float(smooth))) / (math.log(float(article[key] + smooth)) - math.log(float(smooth)))
    return result

def getLogUniqueness(article, smooth=1, returntype=collections.Counter):
    result = returntype()
    for w in article:
        result[w] = math.log(float(article[w] + smooth)) - math.log(float(smooth))
    return result

# !!!!!! Danger !!!!!! Not usable with >1 word long title
def normalizedLogUniqueness(title, smooth=1, returntype=collections.Counter):
    return getLogUnisonUniqueness(getWordCountWiki(title), title.lower(), smooth, returntype)

def compareArticleWithBase(title, listOfTitle, weight=1, smooth=1, returntype=collections.Counter):
    result = returntype()
    N = float(len(listOfTitle)) / weight
    for title2 in listOfTitle:
        cmp = normalizedCompare(title, title2, smooth, returntype)
        for w in cmp:
            result[w] += cmp[w]
    for w in result:
        result[w] /= N
    return result

def expofilter(count, factor, threshold=0):
    wordlist = list(count)
    for w in wordlist:
        if count[w] < threshold:
            del count[w]
        else:
            count[w] = math.exp(factor * count[w])

def getRelativeCount(title, listOfTitle, factor=1, threshold=0, weight=1, smooth=1, returntype=collections.Counter):
    result = compareArticleWithBase(title, listOfTitle, weight, smooth, returntype)
    expofilter(result, factor, threshold)
    return result

# def oddOneOut(article1, article2, article3):
