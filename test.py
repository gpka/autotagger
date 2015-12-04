import wikipedia
import collections
import string
import sys
from math import sqrt
import util


def getPage(title):
    return wikipedia.page(title)

def stripExtraneous(input):
    to_return =  input.replace('\n','')
    to_return = to_return.replace('\u','')
    to_return = to_return.replace('\t','')
    for ch in string.punctuation:
        to_return = to_return.replace(ch,'')
    return to_return

def countFreq(string):
    return collections.Counter(string.split(" "))

def removeMeaningless(count):
    to_remove = {'The', 'the', 'A', 'a', 'is', 'are', 'was', 'were', 'of', 'in',\
     'by', 'for', 'as','at', 'which', 'that', 'to', 'on', 'than', 'into', 'also',\
     'an', 'An', 'For','and','And','with','in', 'from','has','it','In','have'}
    for word in to_remove:
        count[word] = 0
    return count

# def file_writer(features_vec):
#     with open('testFeature.txt', 'w') as f:
#         for feature in features_vec
#         f.write(str(features))

#print stripExtraneous(getPage("Statue of Liberty").content)

def main(argv):
    if len(argv) != 2:
        print >> sys.stderr, "The number of arguments does not match"
        sys.exit(1)

    argv[0] = argv[0].replace('_', ' ')
    argv[1] = argv[1].replace('_', ' ')

    processedStr1 = stripExtraneous(getPage(argv[0]).content)

    feature1 = removeMeaningless(countFreq(processedStr1))

    processedStr2 = stripExtraneous(getPage(argv[1]).content)
    feature2 = removeMeaningless(countFreq(processedStr2))

    print eval(feature1, feature2)

def dotProduct(d1, d2):
    if len(d1) < len(d2):
        return dotProduct(d2, d1)
    else:
        return sum(d1.get(f, 0) * v for f, v in d2.items())

def eval(d1, d2):
	return float(dotProduct(d1, d2))/sqrt(dotProduct(d1,d1))/sqrt(dotProduct(d2,d2))
#print dotProduct(feature1,feature2)


if __name__ == "__main__":
    main(sys.argv[1:])



#file_writer(feature)
