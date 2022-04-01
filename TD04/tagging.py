import os

class lexicalUnit:
  '''represents a lexical unit'''
  def __init__(self,word,lemma,pos):
    self.__word = word # inflected word    
    if lemma == '<unknown>':
      self.__lemma = word
    else:
      self.__lemma = lemma # lemma
    self.__pos = pos # pos (part-of-speech)
  
  def getWord(self):
    '''gets the inflected word of the lexical unit'''
    return self.__word

  def getLemma(self):
    '''gets the lemma of the lexical unit'''
    return self.__lemma

  def getPOS(self):
    '''gets the POS of the lexical unit'''
    return self.__pos

  def __eq__(self,other):
    return self.getWord() == other.getWord() and self.getLemma() == other.getLemma() and self.getPOS() == other.getPOS()

  def __str__(self):    
    return '[%s,%s,%s]'% (self.getWord(),self.getLemma(),self.getPOS())


class taggedText:
  '''represents the class of a tagged text'''
  def __init__(self,file=None,with_treetagger=False,treetagger_path='/home/ens/mconstan/treetagger/',language='english'):
    self.__lexicalUnits = [] # list of the lexical units of the text
    if file is not None:
      if not with_treetagger:
        self.__loadTaggedText(file)
      else:
        self.__tag(file,treetagger_path,language)

  def __loadTaggedText(self,file):
    '''load tagged text in $file$
    each line is a lexical unit: a word, a POS and a lemma (all separated by a tabulation)'''
    f = open(file, 'rU')
    while 1:
      line = f.readline()
      if not line:
        break      
      line = line.rstrip()
      tab = line.split('\t')
      unit = lexicalUnit(tab[0],tab[2],tab[1])
      self.add(unit)
    f.close()

  def __tag(self,file,treetagger_path,language):
    '''open a raw text $file$ written in $language$ and tag it using treetagger located in the directory $treetagger_path$'''
    command = treetagger_path + 'tree-tagger-'+language+' "'+file.__str__()+'"' # command to apply treetagger on text $file$
    out = os.popen(command)
    while 1:
      line = out.readline()
      if not line:
        break
      line = line.rstrip()
      tab = line.split('\t')
      unit = lexicalUnit(tab[0],tab[2],tab[1])
      self.add(unit)
    out.close()


  def save(self,file):
    f = open(file,'wU')
    for u in self.lexicalUnits():
      f.write('%s\t%s\t%s\n'%(u.getWord(),u.getPOS(),u.getLemma()))
    f.close()


  def add(self,unit):
    '''adds the lexical unit $unit$ at the end of the tagged text'''
    self.__lexicalUnits.append(unit)

  def get(self,index):
    '''gets the lexical unit at position $index$ in the tagged text'''
    return self.__lexicalUnits[index]

  def len(self):
    '''gets the number of lexical units in the text'''
    return self.__lexicalUnits.__len__()

  def lexicalUnits(self):
    '''gets the list of lexical units of the tagged text'''
    return self.__lexicalUnits

  def filter(self,posSet):
    '''filters the tagged text: returns a new tagged text with only the lexical units that have a POS belonging to the set of POS $posSet$'''
    tt = taggedText()
    for u in self.lexicalUnits():
       if u.getPOS() in posSet:
         tt.add(u)
    return tt

  
  def getTextForChunking(self):
    res = []
    for u in self.lexicalUnits():
      res.append((u.getWord(),u.getPOS()))
    return res


  def getRawText(self):
    s = ''
    i = 0
    n = self.len()
    for u in self.lexicalUnits():
      s += u.getWord()
      if i is not n - 1:
        s += ' '
      i += 1
    return s

  def getWordList(self):
    l = []
    for u in self.lexicalUnits():
      l.append(u.getLemma())
    return l

  def eval(self,tt):
    '''evaluation of the tagged text in comparison with a golden tagged text $tt$
    a tag is correct if the POS of a word is the same as the one in $tt$
    returns the precision of the tagged text'''
    n = self.len()
    cnt = 0.0
    for i in range(0,self.len()):
      u = self.get(i)
      v = tt.get(i)
      if u.getPOS() == v.getPOS():
        cnt += 1
    return cnt/n


  def __str__(self):
    s = ''
    for u in self.lexicalUnits():
      s += u.__str__()
    return s
