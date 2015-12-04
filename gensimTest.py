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

url = 'http://mattmahoney.net/dc/'
def maybe_download(filename, expected_bytes):
  """Download a file if not present, and make sure it's the right size."""
  if not os.path.exists(filename):
    filename, _ = urllib.urlretrieve(url + filename, filename)
  statinfo = os.stat(filename)
  if statinfo.st_size == expected_bytes:
    print('Found and verified', filename)
  else:
    print(statinfo.st_size)
    raise Exception(
        'Failed to verify ' + filename + '. Can you get to it with a browser?')
  return filename
filename = maybe_download('text8.zip', 31344016)
# Read the data into a string.
def read_data(filename):
  f = zipfile.ZipFile(filename)
  for name in f.namelist():
    return f.read(name).split()
  f.close()
words = read_data(filename)
print('Data size', len(words))

def getPage(title):
    return wikipedia.page(title)

def stripExtraneous(input):
    to_return =  input.replace('\n','')
    to_return = to_return.replace('\u','')
    to_return = to_return.replace('\t','')
    for ch in string.punctuation:
        to_return = to_return.replace(ch,'')
    return to_return

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


sentences =  util.generateSentences(words)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
model = gensim.models.Word2Vec(sentences, min_count=1)

model.save('gensimModel')

# if __name__ == "__main__":
#     main(sys.argv[1:])



#file_writer(feature)
