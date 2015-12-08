import collections, math, wikipedia, string, random
############ wikipedia part starts here #############

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
    return stripExtraneous(wikipedia.page(title).content.lower())

def getWordCountWiki(title):
    return collections.Counter(getCleanWikiContent(title).split())

############ wikipedia part ends here ##############
############ processing starts here ###############

def removeMeaningless(count):
    to_remove = ['the', 'of', 'and', 'a', 'an', 'to', 'in', 'is', 'that', 'it', 'are', 'was', 'were',\
     'by', 'for', 'as','at', 'which', 'that', 'on', 'than', 'also', 'as', 'with', 'you', 'they',\
     'be','this', 'from','has','have','or','had','but','not','each','will','about','so', 'can', 'out',\
     'each','which','do', 'would','there','s','its','other','their']
    for word in to_remove:
        del count[word]
    return count

def dotProduct(d1, d2):
    if len(d1) < len(d2):
        return dotProduct(d2, d1)
    else:
        return sum(d1.get(f, 0) * v for f, v in d2.items())

def evaluate(d1, d2):
	return float(dotProduct(d1, d2))/math.sqrt(dotProduct(d1,d1))/math.sqrt(dotProduct(d2,d2))

############ Dataset class #################

class oddOneOut:

    def __init__(self):
        self.dataset = dict()
        self.namelist = []

    def addArticle(self, title):
        raise Exception("This function needs to be overridden.")

    def getOddArticle(self, triple):
        raise Exception("This function needs to be overridden.")

    def getFullTrainingSet(self):
        result = []
        num = len(self.namelist)
        for i in range(0,num):
            # Sample three distinct articles
            for j in range(0,i):
                for k in range(0,j):
                    threearticles = (self.namelist[i], self.namelist[j], self.namelist[k])
                    oddindex, confidence = self.getOddArticle(threearticles)
                    result.append((threearticles, oddindex, confidence))
        return result

    def getPartialTrainingSet(self, num=0):
        result = self.getFullTrainingSet()
        return sorted(result, key=lambda x : x[2], reverse=True)[0:num]

class oddityDot(oddOneOut):
    def addArticle(self, title):
        self.dataset[title] = removeMeaningless(getWordCountWiki(title))
        self.namelist.append(title)

    def getOddArticle(self, triple):
        dots = [evaluate(self.dataset[triple[1]], self.dataset[triple[2]]),
                evaluate(self.dataset[triple[0]], self.dataset[triple[2]]),
                evaluate(self.dataset[triple[0]], self.dataset[triple[1]])]
        sdot = sorted(dots)
        return (dots.index(max(dots)), math.log(float(sdot[2])/math.sqrt(sdot[1] * sdot[0])))
