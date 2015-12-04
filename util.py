import collections
import math
import gensim as gs
import wikipedia
import string

def getPage(title):
    return wikipedia.page(title)

def stripExtraneous(input):
    to_return =  input.replace('\n',' ')
    to_return = to_return.replace('\u',' ')
    to_return = to_return.replace('\t',' ')
    for ch in string.punctuation:
        to_return = to_return.replace(ch,' ')
    return to_return

def getCleanWikiContent(title):
    return stripExtraneous(wikipedia.page(title).content)

def removeMeaningless(text):
    to_remove = {'The', 'the', 'A', 'a', 'is', 'are', 'was', 'were', 'of', 'in',\
     'by', 'for', 'as','at', 'which', 'that', 'to', 'on', 'than', 'into', 'also',\
     'an', 'An', 'For','and','And','with','in', 'from','has','it','In','have', '', 'or', 'be'\
     ,'there', 'their'}
    if type(text) == collections.Counter:
        for word in to_remove:
            text[word] = 0
        return text
    elif type(text) == list:
        return [word for word in text if word not in to_remove]
    else:
        raise Exception("type error. Expected list or counter")

# This will modify a lexicon to get an effective frequency
def toEffectiveFrequency(lex, threshold):
    for words in lex:
        lex[words] = lex[words] - math.sqrt(threshold * lex[words])

# Return a "new" dict or a counter of a lexicon
def getEffectiveFrequency(lex, threshold, returntype='dict'):
    if returntype=='dict' or returntype=='Dict':
        result = dict()
    elif returntype=='Counter' or returntype=='counter':
        result = collections.Counter()
    else:
        raise Exception('returntype must be dict or Counter')
    for words in lex:
        result[words] = lex[words] - math.sqrt(threshold * lex[words])
    return result

# Compute cosine angularity with threshold, looking up wordvectors
def oldFindCountersCosineFromDict(avec1, avec2, threshold, wordvector):
    numer = 0
    denom = 0
    for word1 in avec1:
        for word2 in avec2:
            denom += avec1[word1] * avec2[word2]
            if dot(wordvector[word1], wordvector[word2]) >= threshold:
                numer += avec1[word1] * avec2[word2]
    return numer / denom

# Compute dot product if type matches
def dot(vec1, vec2):
    if type(vec1)==list and type(vec2)==list:
        if len(vec1) != len(vec2):
            raise Exception("Vector must be of the same length.")
        result = 0
        for i in range*len(vec1):
            result += vec1[i] * vec2[i]
        return result
    if (type(vec1)==dict or type(vec1)==collections.Counter) and (type(vec2)==dict or type(vec2)==collections.Counter):
        result = 0
        if type(vec2)==dict:
            for e in vec1:
                if e in vec2:
                    result += vec1[e] * vec2[e]
            return result
        else:
            for e in vec1:
                result += vec1[e] * vec2[e]
            return result
    raise Exception("Type does not match, or type error. Must be list, dict, or Counter")

# Compute cosine between two word vectors. Take two numpy arrays as an input.
# Return value ranging from 0 to 1
def oldFindWordsCosine(wvec1, wvec2):
    import numpy as np
    return np.dot(wvec1, wvec2)/(np.linalg.norm(wvec1)*np.linalg.norm(wvec2))


def norm(wvec):
    import numpy as np
    return np.linalg.norm(wvec)

# Compute cosine value from gensim
def findCosine(avec1, avec2, model, threshold=0.5):
    numer = 0
    denom = 0
    for word1 in avec1:
        for word2 in avec2:
            denom += avec1[word1] * avec2[word2]
            if word1 == word2:
                numer += avec1[word1] * avec2[word2]
            elif word1 in model.vocab and word2 in model.vocab and\
                model.similarity(word1, word2) >= threshold:
                numer += avec1[word1] * avec2[word2]
    return float(numer) / denom

# Compute cosine value from gensim
def findCosineShort(avec1, avec2, model):
    numer = 0
    denom = 0
    for word1 in avec1:
        for word2 in avec2:
            denom += avec1[word1] * avec2[word2]
            if word1 == word2:
                numer += avec1[word1] * avec2[word2]
            elif word1 in model.vocab and word2 in model.vocab:
                numer += avec1[word1] * avec2[word2] * model.similarity(word1, word2)
    return float(numer) / denom

# Compute cosine value from gensim
def oldFindCountersCosine(avec1, avec2, threshold, model, numpyOn=True):
    import numpy
    numer = 0
    denom = 0
    for word1 in avec1:
        for word2 in avec2:
            denom += avec1[word1] * avec2[word2]
            if not numpyOn:
                if model.similarity(word1, word2) >= threshold:
                    numer += avec1[word1] * avec2[word2]
            elif numpy.dot(wordvectorlist[wordlist.index(word1)], wordvectorlist[wordlist.index(word2)]) >= threshold:
                    numer += avec1[word1] * avec2[word2]
    return numer / denom


# Take a string as an input and return a list of sentences. A sentence is a list of words
def generateSentences(wordList):
    #wordList = list(text.split(' '))
    sentences = []
    count = 1
    sentence = []
    for word in wordList:
        if count % 10 == 0:
            sentences.append(sentence)
            sentence = []
        sentence.append(word)
        count += 1
    return sentences


########################################################################
# Cut article
########################################################################

# Take in a list of Counter, percentage = r, number of appearance = n
# Return a list of words that appears strictly more than n time in > r*all articles
# suitable if only want to know common words
def getCommonWords(articleCounters, r, n):
    trackExceed = collections.Counter()
    for article in articleCounters:
        for word in article:
            if article[word] > n:
                trackExceed[word] += 1
    numArticles = len(articleCounters)
    return [w for w in trackExceed if trackExceed[w] > r * numArticles]

# Take in a list of lists, percentage = r, number of appearance = n
# Return a list of words that appears strictly more than n time in > r*all articles
# suitable if only want to know common words
def getCommonWordsFromList(articleLists, r, n):
    articleCounters = [collections.Counter(l) for l in articleLists]
    return getCommonWords(articleCounters, r, n)

# This removes words appearing in a given list from Counters.
# suitable if only want to proceed with prior knowledge about common words
def removeWordsFrom(articleCounters, words):
    if type(articleCounters) == collections.Counter:
        for w in words:
            del articleCounters[w]
    else:
        for w in words:
            for articles in articleCounters:
                del articles[w]

# This removes words appearing in a given list. Returns a new list !!!
# suitable if only want to proceed with prior knowledge about common words
def removeWordsFromList(articleLists, words):
    articleCounters = [collections.Counter(l) for l in articleLists]
    removeWordsFrom(articleCounters, words)
    return [list(c.elements()) for c in articleCounters]

# Combine All above. Modify counter
def autoTruncate(articleCounters, r, n):
    wordlist = getCommonWords(articleCounters, r, n)
    removeWordsFrom(articleCounters, wordlist)

# Combine all above. Returns a new list.
def truncatedList(articleLists, r, n):
    articleCounters = [collections.Counter(l) for l in articleLists]
    autoTruncate(articleCounters, r, n)
    return [list(c.elements()) for c in articleCounters]

# Given a long text, break into sentencess
def toSentences(s):
    # \n
    x1 = s.split('\n')
    x2 = []
    x3 = []
    for tokens in x1:
        x2 += tokens.split('. ')
    for tokens in x2:
        if len(tokens) > 1:
            x3 += [stripExtraneous(tokens).split()]
    return x3

# get article as sentences (Fairly clean, but still contains weird characters)
def getWikiSentences(title):
    return toSentences(wikipedia.page(title).content.lower())
