import random

class Kanji:
  
  def __init__(self,kanji,kun,on,name,marked):
    self.kanji = kanji
    self.kun = kun
    self.on = on
    self.name = name
    self.marked = marked

  ##sets
  def setKanji(self,kanji):
    self.kanji = kanji
  def setKun(self,kun):
    self.kun = kun
  def setOn(self,on):
    self.on = on
  def setName(self,name):
    self.name = name
  def setMarked(self,marked):
    self.marked = marked
  ##gets
  def getKanji(self):
    return self.kanji
  def getKun(self):
    return self.kun
  def getOn(self):
    return self.on
  def getName(self):
    return self.name
  def getMarked(self):
    return self.marked



class KanjiTest:
  
  def __init__(self, testArray, currentIndex, tested, repeat):
    self.testArray = testArray
    self.currentIndex = currentIndex
    self.tested = tested
    self.repeat = repeat

  def appendTestArray(self, ele):
    self.testArray.append(ele)

  def checkAllTested(self):
    if self.tested == len(self.testArray):
      return True
    else:
      return False

  def getNewKanji(self):
    isNew = False
    while isNew == False:
      randKanjiIndex = random.randint(0,len(self.testArray)-1)
      if self.repeat == False:
        if self.testArray[randKanjiIndex].getMarked() != True:
          isNew = True
          self.tested+=1
          self.testArray[randKanjiIndex].setMarked(True)
      else:
        isNew = True

    self.currentIndex = randKanjiIndex
    return randKanjiIndex




  #not sure if this works but its not needed *yet*
  #def replaceTestArrayAtIndex(index,ele):
  #  self.testArray[index].replace(ele)


  ## sets
  def setTested(self,tested):
    self.tested = tested

  def setCurrentIndex(self, index):
    self.currentIndex = index

  def setTestArray(self,testArray):
    self.testArray = testArray 

  def setRepeat(self,repeat):
    self.repeat = repeat

  ## gets
  def getTested(self):
    return self.tested

  def getCurrentIndex(self):
    return self.currentIndex

  def getTestArray(self):
    return self.testArray
  
  def getTestArrayEle(self,index):
    return self.testArray[index]

  def getRepeat(self):
    return self.repeat

