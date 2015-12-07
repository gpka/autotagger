import math, collections
import wikipedia
from util import getWordCountWiki, dot

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

def linfilter(count, threshold=0):
    wordlist = list(count)
    for w in wordlist:
        if count[w] < threshold:
            del count[w]

def getRelativeCount(title, listOfTitle, factor=1, threshold=0, weight=1, smooth=1, returntype=collections.Counter):
    result = compareArticleWithBase(title, listOfTitle, weight, smooth, returntype)
    expofilter(result, factor, threshold)
    return result


################################################################################
def oddOneOut1(title1, title2, title3, factor=1, threshold=0, weight=1, smooth=1, returntype=collections.Counter):
    namelist = [title1, title2, title3]
    cmp1 = getRelativeCount(namelist[0], namelist, factor, threshold, weight, smooth, returntype)
    cmp2 = getRelativeCount(namelist[1], namelist, factor, threshold, weight, smooth, returntype)
    cmp3 = getRelativeCount(namelist[2], namelist, factor, threshold, weight, smooth, returntype)
    common12 = dot(cmp1,cmp2)
    common13 = dot(cmp1,cmp3)
    common23 = dot(cmp2,cmp3)
    print title1, "has odd factor of", common23
    print title2, "has odd factor of", common13
    print title3, "has odd factor of", common12

# perform dot analysis, but pre filter
def getOddity2(namelist, threshold=0):
    cmp12 = normalizedCompare(namelist[1], namelist[0])
    cmp13 = normalizedCompare(namelist[2], namelist[0])
    linfilter(cmp12, threshold)
    linfilter(cmp13, threshold)
    # print cmp12
    # print cmp13
    return dot(cmp12, cmp13)

def oddOneOut2(namelist, threshold=0):
    result = []
    for i in range(3):
        result.append(getOddity2([namelist[i], namelist[(i+1)%3], namelist[(i+2)%3]], threshold))
    return result.index(max(result))
