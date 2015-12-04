import wikipedia
import collections
import string
import sys
from math import sqrt
import util
import gensim as gs


def main(argv):
    if len(argv) != 2:
        print >> sys.stderr, "The number of arguments does not match"
        sys.exit(1)

    argv[0] = argv[0].replace('_', ' ')
    argv[1] = argv[1].replace('_', ' ')
    model = gs.models.Word2Vec.load('gensimModel')

    processed1, processed2 = getPageInstance(argv[0], argv[1])
    # feature1 = removeMeaningless(countFreq(processedStr1))
    # feature2 = removeMeaningless(countFreq(processedStr2))

    #print compareSentence(processed1, processed2, model)
    #print compareArticle(processed1, processed2, model, 0.5)
    print compareSentence(processed1, processed2, model)







def getPage(title):
    return wikipedia.page(title)

def stripExtraneous(input):
    to_return =  input.replace('\n','')
    to_return = to_return.replace('\u','')
    to_return = to_return.replace('\t','')
    # to_return = to_return.replace('=','')
    # to_return = to_return.replace(';','')
    # to_return = to_return.replace(',','')
    # to_return = to_return.replace('.','')
    # to_return = to_return.replace('\'','')
    # to_return = to_return.replace('-','')
    for ch in string.punctuation:
        to_return = to_return.replace(ch,'')
    return to_return

def countFreq(string):
    return collections.Counter(string.lower().split(" "))

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

def getPageInstance(prompt1, prompt2):
    return (stripExtraneous(getPage(prompt1).content), stripExtraneous(getPage(prompt2).content))

def compareArticle(art1, art2, model, threshold):
    count1 = countFreq(art1)
    count2 = countFreq(art2)

    # Remove meaningless words
    # May remove later
    feature1 = removeMeaningless(count1)
    feature2 = removeMeaningless(count2)
    return util.findCosine(feature1, feature2, model, threshold)

def compareSentence(sen1, sen2, model):
    count1 = countFreq(sen1)
    count2 = countFreq(sen2)

    # Remove meaningless words
    # May remove later
    feature1 = removeMeaningless(count1)
    feature2 = removeMeaningless(count2)
    return util.findCosineShort(feature1, feature2, model)

if __name__ == "__main__":
    main(sys.argv[1:])
