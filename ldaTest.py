import gensim as gs
import collections
import util
import string
import sys

# text1 = "eat pizza apple sauce food yummy delicious"
# text2 = "tomato pizza food italian delicious eat"
# text3 = "dog cat pet cute kitty puppy love nature"
# text4 = "eat dog cat food puppy love"
# documents = [text1, text2, text3, text4]
# texts = [document.lower().split(" ") for document in documents]

listOfPageName = ['Red','Green','Blue','Black','White','Brown','Pink','Gray','Thailand', 'Japan', 'Qatar', 'India', \
'China', 'Vietnam', 'Singapore', 'Malaysia', 'Indonesia', 'Dog', 'Cat', 'Pig', 'Cow', 'Bird', 'Lion', 'Elephant',\
'Fish', 'Snake']

pages = [util.getCleanWikiContent(names) for names in listOfPageName]

texts = [util.removeMeaningless(page.lower().split(' ')) for page in pages]
dictionary = gs.corpora.Dictionary(texts)

d = dict()
for k,v in dictionary.items():
    d[k] = v
corpus = [dictionary.doc2bow(text) for text in texts]
lda = gs.models.ldamodel.LdaModel(corpus, num_topics=8)

topic0 =  lda.get_topic_terms(0)
topic1 =  lda.get_topic_terms(1)
topic2 =  lda.get_topic_terms(2)
topic3 =  lda.get_topic_terms(3)
topic4 =  lda.get_topic_terms(4)
topic5 =  lda.get_topic_terms(5)
topic6 =  lda.get_topic_terms(6)
topic7 =  lda.get_topic_terms(7)
for worddex, prob in topic0:
    print d[worddex], prob
print
for worddex, prob in topic1:
    print d[worddex], prob
print
for worddex, prob in topic2:
    print d[worddex], prob
print
for worddex, prob in topic3:
    print d[worddex], prob
print
for worddex, prob in topic4:
    print d[worddex], prob
print
for worddex, prob in topic5:
    print d[worddex], prob
print
for worddex, prob in topic6:
    print d[worddex], prob
print
for worddex, prob in topic7:
    print d[worddex], prob
# print lda.print_topic(1)
# print gs.corpora.Dictionary.from_corpus(corpus)
