from tagging import taggedText
from textSpaceVector import textVector

class wsdData:

  def __init__(self,file,filter,word):
    tt = taggedText(file=file,with_treetagger=True,treetagger_path='/home/ens/mconstan/treetagger/')
    self.__instances = self.__splitText(filter,tt)
    self.__ambiguousWord = word  # ambiguous word to deal with
    self.__textInstances = self.computeTextInstances()
  

  def __splitText(self,filter,tt):
    '''This function splits the tagged text $tt$  in several parts (separator is the form '------'), 
    applies a filter on the POS ($filter$)
    and returns a list of lists of words that passed the filter'''
    t = tt.filter(filter)
    list = t.getWordList()
    i = 0
    ll = []
    ll.append([])
    for w in list:
      if w == '------':
        i += 1
        ll.append([])
      else:
        ll[i].append(w)
    return ll


  def getInstances(self):
    return self.__instances


  def getTextInstances(self):
    return self.__textInstances


  def getAmbiguousWord(self):
    return self.__ambiguousWord

  def computeTextInstances(self):
    instances = self.getInstances()
    textInstances = []
    for instance in instances:
      text = ''
      for w in instance:
        if w != self.getAmbiguousWord():
          text += ' '+w
      textInstances.append(text)
    return textInstances


  def getInstanceVectors(self):
    instances = self.getTextInstances()
    ivectors = []
    for i in instances:      
      ivectors.append(textVector(text=i))
    return ivectors
