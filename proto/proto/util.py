import json



##funciton to turn a knaji char into its utf-8 ascii rep for a url
def kanji_to_utf8_ascii_url_string(kanji):
  
  #list of chars to remove from kanji
  expell = ["x","\'"] 
  #encodes turns to string, then removes the first 4 chars of the string
  kanji = kanji.encode("utf-8")
  kanji = str(kanji)
  kanji = kanji[4:]

  #removes uneeded chars
  for i in kanji:
    if i in expell:
      kanji=kanji.replace(i,"")
    elif i == "\\":
      kanji=kanji.replace(i,"%")
    else:
      kanji=kanji.replace(i,i.upper())
  #adds % at the start
  kanji = "%" + kanji

  return kanji

#creates grade JSON txt files

#ctrl+k+C to comment
#ctrl+k+u to uncomment

#def createGradeJSONFiles():
#  #grade = "grade-"
#  #for i in range(1,8):
#  #  if i == 7:
#  #    i = 8
#    #currentGrade = i
#    #gradeName = grade + str(currentGrade) + ".txt"
#    #data = req.get_kanji_grade_data(i)
#    #print(data) ##testing

#  #accept kun, on, name and custumn


#  grade = "grade-"
#  TOTALKANJI = 0
#  for i in range(1,8):#一
#    data = {}
#    data['kanji'] = []
#    if i == 7:
#      i = 8
  
#    currentGrade = i
#    gradeName = grade + str(currentGrade) + ".txt"
#    gradeList =  grade + str(currentGrade)
#    listData = req.get_kanji_list_data(gradeList)

#    kanjiCharReadings = []
#    print(listData)
#    num = 1
#    for kanji in listData:
#      print(kanji)
#      kanjiData = req.get_kanji_char_data(kanji)
#      kun = kanjiData["kun_readings"],
#      on = kanjiData["on_readings"],
#      name = kanjiData["name_readings"]
#      print("###########################################################################")
#      print("Grade is " + str(currentGrade))
#      print(num)
#      print("###########################################################################")
#      data['kanji'].append({
#        'kanji': kanji,
#        'kun' : kun,
#        'on' : on,
#        'name' : name
#        })
#      num+=1
#    with open(gradeName,"w") as outfile:
#      json.dump(data, outfile,indent=4)
#    TOTALKANJI+=num
#    if i == 8:
#      break
#  print("#########################")
#  print("#########################")
#  print("Totoal number of kanji added are:")
#  print(TOTALKANJI)
#  print("#########################")
#  print("#########################")
#createGradeJSONFiles()













##gets all chars from a text file
def getCharsFromtxt(file):
    chars = []
    for line in file:
      for char in line:
        chars.append(char)
    return chars