import numpy as np
import util
import collections
import pickle

# Read data from pickle files

f1 = open('dictionary_simple.pckl', 'r')
f2 = open('vec_simple.pckl', 'r')
dic = pickle.load(f1)
vecs = pickle.load(f2)
f1.close()
f2.close()
wordlist = list(dic.keys())

str1 = 'king'
str2 = 'queen'
str3 = 'food'
str4 = 'tree'
# vec1 = vecs[wordlist.index(str1)]
# vec2 = vecs[wordlist.index(str2)]
# vec3 = vecs[wordlist.index(str3)]
# vec4 = vecs[wordlist.index(str4)]
#print(util.findWordsCosine(vec1, vec2))
print(util.norm(vec2))
print(np.dot(vec1,vec3))
