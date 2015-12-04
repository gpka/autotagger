import wikipedia
import collections
import string
import sys
from math import sqrt
import util
import gensim, logging
import os
import urllib
import zipfile
import pickle

f1 = open('gensimModel.pckl', 'rb')
model = pickle.load(f1)
f1.close()

def main(argv):
    if len(argv) != 2:
        print >> sys.stderr, "The number of arguments does not match"
        sys.exit(1)

    argv[0] = argv[0].replace('_', ' ')
    argv[1] = argv[1].replace('_', ' ')
    print model.similarity(argv[0], argv[1])

if __name__ == "__main__":
    main(sys.argv[1:])
