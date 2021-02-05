import PySimpleGUI as sg
import json
import urllib.request
import util
import req
import os
import random
import time
from kanjiClass import Kanji, KanjiTest
##from PIL import Image

#import sys
#import codecs
#######################################
#https://kanjiapi.dev/
#######################################

###theme decider
  #layout = [[sg.Text('Theme Browser')],
  #          [sg.Text('Click a Theme color to see demo window')],
  #          [sg.Listbox(values=sg.theme_list(), size=(20, 12), key='-LIST-', enable_events=True)],
  #          [sg.Button('Exit')]]

  #window = sg.Window('Theme Browser', layout)

  #while True:  # Event Loop
  #    event, values = window.read()
  #    if event in (sg.WIN_CLOSED, 'Exit'):
  #        break
  #    sg.theme(values['-LIST-'][0])S
  #    sg.popup_get_text('This is {}'.format(values['-LIST-'][0]))

  #window.close()


def mainWindow():
  sg.theme('BrightColors')
  mainLayout = [ [sg.Text("Which Grade")],
            [sg.ReadButton("Test Grade 1",key="gradeTest1"),sg.Radio('Only Kun Reading', "choice", default=True, key = "kunRead")],#sg.Checkbox('kun Readings', default=True,key="kunRead"), sg.Checkbox('On Readings', key="onRead")],
            [sg.ReadButton("Test Grade 2",key="gradeTest2"),sg.Radio('Only On Reading', "choice", default=False, key="onRead")],
            [sg.ReadButton("Test Grade 3",key="gradeTest3"),sg.Radio('Both Readings', "choice", default=False, key="bothRead")],
            [sg.ReadButton("Test Grade 4",key="gradeTest4")],
            [sg.ReadButton("Test Grade 5",key="gradeTest5")],
            [sg.ReadButton("Test Grade 6",key="gradeTest6")],
            [sg.ReadButton("Test Grade 8",key="gradeTest8")],
            ]

  MainWindow = sg.Window('Kanji Test', mainLayout,size=(400, 300),
                       return_keyboard_events=True, use_default_focus=False)

  grades= ["gradeTest1","gradeTest2","gradeTest3","gradeTest4","gradeTest5","gradeTest6","gradeTest8"]

  while True:
    event, values = MainWindow.Read()
    if event == sg.WIN_CLOSED:
      break
    for i in range(0,len(grades)):
      if event == grades[i]:
        if values["bothRead"] == False:
          isKunReading = values["kunRead"]
          isOnReading = values["onRead"]
        else:
          isKunReading = True
          isOnReading = True

        gradeNum = grades[i][-1:]
        #print(gradeNum)
        #print(isKunReading)
        #print(isOnReading)
        test = kanjiGradePrac(gradeNum,isKunReading,isOnReading)
        if len(test ) == 1:
          print("TEST WORKED")
        else:
          sg.Popup('Your Score, out of ' + str(test[1]) + ' shown was:',
          'Correct: ' + str(test[0]),
          'Wrong: ' + str(test[2]))
        

def kanjiGradePrac(grade,isKunReading,isOnReading):#kunReading,onReading,nameReadings:

  _STATE_ = {
  "running" : False
  }
  sg.theme('BrightColors')
  layout = [ [sg.Text("Kanji reading is:",justification='center', size = (62,1),font=('Helvetica 20'))],
            [sg.Text("", size = (7,1)),sg.Text("", size=(13,1),key="kanjiReading",justification='center',font=('Helvetica 20'))],
            [sg.Text("", size = (7,1)),sg.InputText(justification='center',size=(13,1), key="userKanji",font=('Helvetica 20'))],
            [sg.Text("", size = (10,1)),sg.Text("",size = (20,1),key="answer",font=('Helvetica 20'))],
            [sg.Text("", size = (15,1)), sg.ReadButton("Start", key="butStart"), 
             sg.Button('submit', visible=False, bind_return_key=True)],
            [sg.Text("Correct", size = (6,1), justification='center',font=('Helvetica 14')),
             sg.Text("", size = (3,1)),
             sg.Text("Shown",size = (6,1), justification='center',font=('Helvetica 14')),
             sg.Text("", size = (4,1)),
             sg.Text("Wrong",size = (6,1),justification='center',font=('Helvetica 14'))],
            [sg.Text("0", size = (6,1), justification='center',key="correct",font=('Helvetica 14')),
             sg.Text("", size = (3,1)),
             sg.Text("0",size = (6,1), justification='center',key="shown",font=('Helvetica 14')),
             sg.Text("", size = (4,1)),
             sg.Text("0",size = (6,1),justification='center',key="wrong",font=('Helvetica 14'))],
            ]
  
  window = sg.Window('Kanji Test', layout,size=(350, 280),
                     return_keyboard_events=True, use_default_focus=False)


  ##get all kanji from grade file as data
  gradeNum = str(grade)
  filePath = "grades\grade-" + gradeNum + ".txt"
  with open(filePath) as json_file:
    data = json.load(json_file)
  
  ##kanjiArray were each element in a dictionary holding 1 kanji and its readings
  ##has a boolean "marked" key, this is in use to see if the kanji has been tested before
  kanjiTestArray = KanjiTest([],-1,0,False)
  for i in range(0,2):#for i in data["kanji"]:
    #kanjiObj = Kanji(i["kanji"],i["kun"][0],"サ",i["name"],False)
    #testing with a shorter range
    kanjiObj = Kanji(data["kanji"][i]["kanji"],data["kanji"][i]["kun"][0],data["kanji"][i]["on"][0],data["kanji"][i]["name"],False)#data["kanji"][i]["kun"][0],"サ",data["kanji"][i]["name"],False)
    kanjiTestArray.appendTestArray(kanjiObj)

  currentKanjiIndex = kanjiTestArray.getNewKanji()

  print("current kanji index is: " + str(currentKanjiIndex))


  #numbers tracking user's score
  shown = 0
  correct = 0
  wrong = 0
  score = [0]

  shownBefore = False
  passedKanji = False
  #event loop
  while True:
    event, values = window.Read()

    #closes loop
    if event == sg.WIN_CLOSED:
      break
        
    #starts test loop
    if event == "butStart":
      _STATE_["running"] = True
    

    print(str(_STATE_["running"]))#testing
    
    # only takes users input when
    # enter key is pressed
    if event == "submit":
      userKanji = values["userKanji"]
    else:
       userKanji = ""

    #currentKanjiIndex = kanjiTestArray.getNewKanji()
    if _STATE_["running"] == True:
      #shows current kanji
      window["kanjiReading"].Update(kanjiTestArray.getTestArrayEle(currentKanjiIndex).getKanji())

      #checks if usersreading is in on
      correctAnswer = False
      if userKanji != "":
        if isKunReading == True:
          if userKanji in kanjiTestArray.getTestArrayEle(currentKanjiIndex).getKun():
            correctAnswer = True
            print("kun yes")
          else:
            correctAnswer  = False
            print("kun no")
        if isOnReading == True and correctAnswer != True:
          print(kanjiTestArray.getTestArrayEle(currentKanjiIndex).getOn())
          print(userKanji)
          if userKanji in kanjiTestArray.getTestArrayEle(currentKanjiIndex).getOn():
            correctAnswer = True
            print("on yes")
          else:
            correctAnswer = False
            print("on no")
        if correctAnswer == True:
          #displays correct answer
          answer = userKanji + "is correct"
          window.FindElement("answer").Update(answer) #kunReading,onReading,nameReadings
          #clear users input
          window["userKanji"]("")
          shown+=1
          passedKanji = True
        if passedKanji == True:
          if shownBefore != False:
            wrong+=1
            #selcect new kanji
            #randKanjiIndex = random.randint(0,len(kanjiTestArray)-1) 
            #currentKanji = kanjiTestArray[randKanjiIndex]
            if kanjiTestArray.getRepeat() == False: 
              if kanjiTestArray.checkAllTested() == True:
                print("all have been tested")
                break
            currentKanjiIndex = kanjiTestArray.getNewKanji()
            #reset bool tests
            shownBefore = False
            passedKanji = False
          else:
            correct+=1
            #print(testedKanji)
            #print(currentKanjiIndex)
            #select new kanji
            #randKanjiIndex = random.randint(0,len(kanjiTestArray)-1) 
            #currentKanji = kanjiTestArray[randKanjiIndex]
            if kanjiTestArray.getRepeat() == False: 
              if kanjiTestArray.checkAllTested() == True:
                print("all have been tested")
                score = [correct, shown, wrong]
                break
            currentKanjiIndex = kanjiTestArray.getNewKanji()
            #reset bool tests
            shownBefore = False
            passedKanji = False

          #updates scores for user to see
          window["shown"].Update(shown)
          window["correct"].Update(correct)
          window["wrong"].Update(wrong)
        elif userKanji != "":
          answer = userKanji + "is wrong"
          window["answer"].Update(answer)
          shownBefore = True
  #TODO 
  #pop up wiht button to close both windows, 
  #shows scores on that window          
  #closes window and returns with the array score:
  #                               correct, shown, wrong        
  
  #sg.popup_OK('Score was')


  #time.sleep(0.5)
  window.close()
  return score
          
      

mainWindow()
#kanjiGradePrac("1")

