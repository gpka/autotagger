import math, collections
# get article as sentences (Fairly clean, but still contains weird characters)
def getWikiSentences(title):
    return toSentences(wikipedia.page(title).content.lower())

# Given two article, return a word spectrum. Input must be a Counter.
def getWordUniqueness(article1, article2, smooth=1, returntype=collections.Counter):
    result = returntype()
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

def getWikiUniqueness(title1, title2, smooth=1, returntype=collections.Counter):
    return getWordUniqueness(getWordCountWiki(title1), getWordCountWiki(title2), smooth, returntype)

def getWikiCompareSpectrum(title1, title2, smooth=1, returntype=collections.Counter):
    maxi, mini = float('-inf'), float('inf')
    result = getWikiUniqueness(title1, title2, smooth, returntype)
    for words in result:
        maxi = max(maxi, result[words])
        mini = min(mini, result[words])
    for words in result:
        result[words] = 2 * float(result[words] - mini) / (maxi - mini) - 1
    return result

# OddOneOut model
# def oddOneOut(article1, article2, article3):
