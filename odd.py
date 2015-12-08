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
    to_remove = {'The', 'the', 'A', 'a', 'is', 'are', 'was', 'were', 'of', 'in',\
     'by', 'for', 'as','at', 'which', 'that', 'to', 'on', 'than', 'into', 'also',\
     'an', 'An', 'For','and','And','with','in', 'from','has','it','In','have'}
    for word in to_remove:
        del count[word]
    return count

def LogProbReplace(count, smooth=1):
    total = 0
    for w in count:
        total += count[w]
    for w in count:
        count[w] = math.log(float(count[w] + smooth) / total)
    count["$ref"] = -math.log(float(total) / smooth)

def insertTotal(count):
    total = 0
    for w in count:
        total += count[w]
    count["$total"] = total

def RankReplace(count):
    frequencies = []
    for w in count:
        frequencies.append(count[w])
    frequencies = sorted(frequencies)
    print frequencies
    for w in count:
        count[w] = float(frequencies.index(count[w]) + 1) / len(frequencies)

def filterUncommon(count, lowerBound=3.5):
    words = list(count)
    for w in words:
        if count[w] <= lowerBound:
            del count[w]

def ternaryFilter(count,lowerBound=lambda x : 3.5, upperBound=lambda x : math.sqrt(x.most_common(1)[0][1])):
    words = list(count)
    lower = lowerBound(count)
    upper = upperBound(count)
    for w in words:
        if count[w] < lower:
            del count[w]
        elif count[w] > upper:
            count[w] = 2
        else:
            count[w] = 1

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
        result = []
        for _ in range(num):
            # Sample three distinct articles
            threearticles = tuple(random.sample(self.namelist, 3))
            oddindex, confidence = self.getOddArticle(threearticles)
            result.append((threearticles, oddindex, confidence))
        return result

class oddity1(oddOneOut):

    def addArticle(self, title):
        self.dataset[title] = getWordCountWiki(title)
        self.namelist.append(title)
        LogProbReplace(self.dataset[title])

    def getOddity(self, triple):
        title1, title2, title3 = triple
        words = []
        for w in self.dataset[title1]:
            words.append(w)
        for w in self.dataset[title2]:
            words.append(w)
        for w in self.dataset[title3]:
            words.append(w)
        words = list(set(words))
        for w in words:
            print w, (self.dataset[title1][w] if self.dataset[title1][w] != 0 else self.dataset[title1]["$ref"]),\
                     (self.dataset[title2][w] if self.dataset[title2][w] != 0 else self.dataset[title2]["$ref"]),\
                     (self.dataset[title3][w] if self.dataset[title3][w] != 0 else self.dataset[title3]["$ref"])

class oddityRank(oddOneOut):
    def addArticle(self, title):
        self.dataset[title] = getWordCountWiki(title)
        ternaryFilter(self.dataset[title])
        self.namelist.append(title)
    def getOddity(self, triple):
        def oddityDictionary(a,b,c):
            if (a,b,c)==(0,0,1):
                return (0,0,1)
            elif (a,b,c)==(0,1,0):
                return (0,1,0)
            elif (a,b,c)==(1,0,0):
                return (1,0,0)

            elif (a,b,c)==(1,1,0):
                return (0,0,1)
            elif (a,b,c)==(1,0,1):
                return (0,1,0)
            elif (a,b,c)==(0,1,1):
                return (1,0,0)

            elif (a,b,c)==(0,0,2):
                return (0,0,3)
            elif (a,b,c)==(0,2,0):
                return (0,3,0)
            elif (a,b,c)==(2,0,0):
                return (3,0,0)

            elif (a,b,c)==(2,2,0):
                return (0,0,9)
            elif (a,b,c)==(2,0,2):
                return (0,9,0)
            elif (a,b,c)==(2,2,0):
                return (9,0,0)

            elif (a,b,c)==(1,1,2):
                return (0,0,2)
            elif (a,b,c)==(1,2,1):
                return (0,2,0)
            elif (a,b,c)==(2,1,1):
                return (2,0,0)

            elif (a,b,c)==(2,2,1):
                return (0,0,4)
            elif (a,b,c)==(2,1,2):
                return (0,4,0)
            elif (a,b,c)==(1,2,2):
                return (4,0,0)

            else:
                return (0,0,0)
        odd1,odd2,odd3 = 0,0,0
        title1, title2, title3 = triple
        words = []
        for w in self.dataset[title1]:
            words.append(w)
        for w in self.dataset[title2]:
            words.append(w)
        for w in self.dataset[title3]:
            words.append(w)
        words = list(set(words))
        for w in words:
            increment1, increment2, increment3 = oddityDictionary(self.dataset[title1][w], self.dataset[title2][w], self.dataset[title3][w])
            odd1 += increment1
            odd2 += increment2
            odd3 += increment3
        return (odd1,odd2,odd3)

    def getOddArticle(self, triple):
        threeodds = self.getOddity(triple)
        sortedodds = sorted(threeodds)
        return (threeodds.index(sortedodds[2]), float(sortedodds[2]) / sortedodds[1] - 1)

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
