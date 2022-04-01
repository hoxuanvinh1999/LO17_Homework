import math
import nltk,re,sys
from nltk import tokenize


class textVector:
  '''class textvector that represents a text in the form of a vector'''


  def __init__(self,text = None,file = None,pattern= r'\w+',name = ''):
    '''textVector constructor
    parameter $text$ is a string (text)
    parameter $file$ is a filename
    parameter $pattern$ is the regex to tokenize the text'''
    self.__pattern = pattern # regex to tokenize the text
    self.__tokens = {} #dictionary of tokens (token->frequency in text)
    self.__count = 0 # count of tokens 
    self.__name = name # name (id) of the textVector

    #in the case where text and file are not None, file is loaded

   
    if file is not None:
      self.__loadFile__(file)
      self.__name = file
      return

    if text is not None:
      self.__loadTokenList(text)
 

  def __loadTokenList(self,text):
    '''loads a string text'''
    tokenlist = list(nltk.tokenize.regexp_tokenize(text, self.__pattern))
    self.__count += len(tokenlist)
    for token in tokenlist:
      self.inc(token)


  def __loadFile__(self,filename):
   '''loads document filename'''
   f = open(filename, 'rU')
   text = f.read().lower()
   f.close()
   self.__loadTokenList(text)
     
  def inc(self,token): 
    '''increments the count of token'''    
    self.__tokens[token] = self.__tokens.get(token,0) + 1

  def get(self,token): 
    '''gets the number of occurrences of token'''
    return float(self.__tokens.get(token,0))  
  
  def getTokens(self): 
    '''gets the dictionary of tokens'''
    return self.__tokens

  def setVector(self,v):
    '''sets the dictionary of tokens __tokens to $v$'''
    self.__tokens = v

  def setName(self,name):
    self.__name = name

  def getName(self):
    return self.__name

  def getId(self):
    '''returns the ID of textVector, i.e. its name '''
    return self.__name

  def len(self): 
    '''returns the number of tokens'''
    return self.__count

  def freq(self,token): 
    '''returns the frequency of token'''
    return self.get(token)
  
  def addFreq(self,token,freq):
    '''adds the value $freq$ to the frequency of $token$'''
    self.__tokens[token] = self.__tokens.get(token,0) + freq
  
  
  def printVector(self,with_freq=True,with_idf=False,collection=None):
    '''prints vector representing text'''
    for t in self.getTokens().keys():
      print(t + ':'+ self.getWeight(t,with_freq=with_freq,with_idf=with_idf,collection=collection).__str__())

  def printPoint(self):
    '''prints coordinates of vector representing text'''
    for t in self.getTokens().keys():
      print(t + ':'+ self.freq(t).__str__())


  def norm(self,with_freq = True,with_idf=False,collection=None): 
    '''returns the norm of self in the context of the collection collection (tfidf)'''
    tokens = self.getTokens().keys()
    n = 0.0  
    for token in tokens:
      val = self.getWeight(token,with_freq=with_freq,with_idf=with_idf,collection=collection)     
      n += val*val 
    return math.sqrt(n)

  
  def getWeight(self,token,with_freq=True,with_idf=False,collection=None):
    '''returns the weight of a given token $token$ in the document
    parameter $with_freq$ indicates if occurrence frequency of $token$ is used (if not, binary frequency)
    parameter $with_idf$ indicates if idf is used to compute the weight, in the context of the collection of documents $collection$'''
    freq = self.freq(token)
    if not(with_freq) and self.freq(token) > 0:
      freq = 1
    if collection is None:
      idf = 1.0
    else:
      if with_idf:
        df = collection.getIdf(token)
        ndoc = collection.len()
        if df == 0: df = 1.0
        if ndoc == 0: df = 1.0
        idf = math.log(float(ndoc)/df)
      else:
        idf = 1.0
    return freq*idf



  def scalarProduct(self,vector,with_freq=True,with_idf=False,collection=None):
    '''returns the scalar product of self with another textVector vector
     parameter $with_freq$ indicates if occurrence frequency of $token$ is used (if not, binary frequency)
    parameter $with_idf$ indicates if idf is used to compute the weight, in the context of the collection of documents $collection$'''
    
    prod = 0.0
    # A COMPLETER
    return prod

  def merge(self,v):
    '''returns a new textVector that is the merging of $self$ and vector $v$'''
    m = textVector()
    tokens = v.getTokens()
    for token in tokens:
      f = v.freq(token)
      m.__count += f
      m.addFreq(token,f)
    tokens = self.getTokens()
    for token in tokens:
      f = self.freq(token)
      m.__count += f
      m.addFreq(token,f)
    return m
    

  def sim(self,vector,with_freq=True,with_idf=False,with_norm=True,collection=None):
    '''returns similarity score between self and the textVector vector
    parameter $with_freq$ indicates if occurrence frequency of $token$ is used (if not, binary frequency)
    parameter $with_idf$ indicates if idf is used to compute the weight, in the context of the collection of documents $collection$
    parameter $with_norm$ indicates if normalisation is used'''

    if with_norm:
      return self.scalarProduct(vector,with_freq=with_freq,with_idf=with_idf,collection=collection)/(vector.norm(with_freq=with_freq,with_idf=with_idf,collection=collection)*self.norm(with_freq=with_freq,with_idf=with_idf,collection=collection))
    else:
      return self.scalarProduct(vector,with_freq=with_freq,with_idf=with_idf,collection=collection)


  def __str__(self): return self.__name.__str__()+':'+self.__tokens.__str__()

  def __hash__(self): 
    name = self.__name
    if name == None: return 0
    return self.__name.__hash__()


class textVectorCollection:
  def __init__(self,list=None,file=None,pattern=r'\w+',name = ''):
    '''textVectorCollection constructor.
    parameter $list$ is a list of filenames
    parameter $file$ is a file that contains the list of documents to be loaded (a pathname per line)
    parameter $pattern$ is the regex to tokenize the texts
    parameter $name$ is the name of the collection'''
    self.__vectors = [] # list of textVectors
    self.__tokens = {} # dictionary of tokens (token -> number of documents where token occurs)
    self.__name = name # name of the collection
    self.__pattern = pattern # regex to tokenize the texts
    if file is not None:
      self.loadFromFile(file,pattern)
      return

    if list is not None:
      self.loadVectorsFromFiles(list,pattern)
      return
  

  def loadFromFile(self,file,pattern):
    '''loads the documents listed in file $file$'''
    f = open(file, 'rU')

    while 1:
      # une ligne est composee d'un nom de fichier
      line = f.readline()
      if not line: break
      fname = line.rstrip()
      v = textVector(file = fname,pattern=pattern) # on charge le document $fname$
      self.addVector(v) 
       
    f.close()

  def loadVectorsFromFiles(self,filenames,pattern):
    for filename in filenames:
      v = textVector(file = filename,pattern=pattern)
      self.addVector(v)

  def setName(self,name):
    self.__name = name

  def addVector(self,v):
    self.__vectors.append(v)
    for token in v.getTokens().keys():
      self.__tokens[token] = self.__tokens.get(token,0) + 1

  def printSortedTokens(self):
    '''print tokens with their associated idf, sorted according to these values'''
    tok = self.getTokens().keys()
    tokdic = self.getTokens()
    def sorter(x,y):
     return -cmp(tokdic[x],tokdic[y])

    list = sorted(tok,cmp=sorter)
    for t in list:
      line = t + ':'+self.getIdf(t).__str__()+'/'+self.len().__str__()
      print(line)
 
  def getTokens(self):
    return self.__tokens

  def getIdf(self,token):
    '''gets the number of documents where token $token$ occurs'''
    return self.__tokens.get(token,0)

  def len(self):
    '''gets the number of documents in the collection'''
    return len(self.__vectors)

  def get(self,index): 
    '''gets the $index$-th textVector of the collection'''
    return self.__vectors[index]

  def vectors(self):
    '''returns the list of vectors'''
    return self.__vectors

  def applyQuery(self,query,with_freq=True,with_idf=False,with_norm=True,nbest=10):
    '''apply query $query$ (string) on the collection (self), and keeps the $nbest$ best documents
    parameter $with_freq$ indicates if occurrence frequency of $token$ is used (if not, binary frequency)
    parameter $with_idf$ indicates if idf is used to compute the weight, in the context of the collection of documents $collection$'''


    q = textVector(text=query)
    res = {}
    for i in range(0,len(self.__vectors)):
      v = self.get(i)
      res[v] = v.sim(q,with_freq=with_freq,with_idf=with_idf,with_norm=with_norm,collection=self) 

    def sorter(x,y):
      return -cmp(res[x],res[y])

    list = sorted(self.__vectors,cmp=sorter)
    result = []
    i = 0
    for v in list:
      if i >= nbest:
        return result
      result.append(v.__str__()+'('+res[v].__str__()+')')
      i += 1
    return result
    
  def barycentre(self,all):
    '''compute barycentre of the collection, with idf from collection $all$ '''
    barycentre = textVector()
    mean = {} #dictionary of tokens (token->coordinate)
    tokenlist = self.getTokens().keys()
    for token in tokenlist:
      mean[token]=0.0
    for j in range(0,len(self.__vectors)):
        v = self.get(j)
        norm = v.norm(with_freq=True,with_idf=True,collection=all)
        for token in tokenlist:
           mean[token] += (v.getWeight(token,with_freq=True,with_idf=True,collection=all))/norm
    #no need to divide by $self.len$ since $mean$ will be normalized now
    norm = 0.0  
    for token in tokenlist:
      norm += mean[token]*mean[token]
    norm = math.sqrt(norm)
    for token in tokenlist:
      mean[token] /= norm
    barycentre.setVector(mean)
    barycentre.setName(self.__name)
    return barycentre
  

