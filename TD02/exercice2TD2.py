import nltk
import codecs
import pickle



def getWords(filename):
  f = codecs.open(filename,'r','utf-8')
  text= f.read().lower()
  
  l = nltk.regexp_tokenize(text,"\w+")
  f.close()
  return l

def buildIndex(filename):
  pos = filename.rfind('/')
  prefix = ''
  if pos != -1:
    prefix = filename[:pos]+'/'
    
 
 
  index = {}
  f = open(filename,'r')
  for text in f:      
     text = text[:-1]
     for w in getWords(prefix+text):
        index[w] = index.get(w,set([]))
        index[w].add(text)       
  f.close()   
  return index

if len(sys.argv) != 2:
  print >> sys.stderr, "Usage: python "+sys.argv[0]+" <collection filename>"
  sys.exit()

index = buildIndex(sys.argv[1])
pickle.dump(index,open('index.pckl','w'))
import pickle
import nltk
import sys

def computeAndQuery(queryWords,index):
  result = index.get(queryWords[0],set([]))
  for w in queryWords[1:]:
    result = result.intersection(index.get(w,set([])))
  return result

def computeOrQuery(queryWords,index):
  result = index.get(queryWords[0],set([]))
  for w in queryWords[1:]:
    result = result.union(index.get(w,set([])))
  return result

def computeQuery(query,index):  
  words = nltk.regexp_tokenize(query,"\w+")
  if len(words) == 0:
    return set([])
  if not query.startswith('
  
  '):
    return computeAndQuery(words,index)
  return computeOrQuery(words,index)

index = pickle.load(open/span>('index.pckl'))
while True:
   query = raw_input('Enter a query:')
   print 'RESULT:'
   print computeQuery(query,index) 
   