import json
import urllib.request
from util import kanji_to_utf8_ascii_url_string

#################################################
#https://kanjiapi.dev/ie=UTF-8&/v1/kanji/

#https://kanjiapi.dev/#!/documentation
#################################################


#quick function to check lists
#replaces [] with unknown
def checkLists(list):
  length = len(list)
  for i in range(0,length):
    if list[i] == []:
      list[i] = "unknown"
  return list

#gets data for an individual kanji

def get_kanji_char_data(kanji):
  #base api link
  api_kanji_link = "https://kanjiapi.dev/v1/kanji/"

  #gets knaji ready for url
  urlKanji = kanji_to_utf8_ascii_url_string(kanji)


  #open link and get request
  #returns 404 if theres an HTTP Error
  try:
    with urllib.request.urlopen(api_kanji_link + urlKanji) as res:
      response = res.read()
  except urllib.error.HTTPError as exception:
    print(exception)
    return 404
  #decode response into utf-8 and then load json as a python obj
  decoded_response = response.decode("utf-8")
  obj = json.loads(decoded_response)

  #checks that grade, heisign_en and jlpt are not null
  if obj["grade"] is None:
    grade = "No Grade"
  else:
    grade = obj["grade"]

  if obj["heisig_en"] is None:
    heisig_en = "No Heisig keyword"
  else:
    heisig_en = obj["heisig_en"]

  if obj["jlpt"] is None:
    jlpt = "No JLPT Test Level"
  else:
    jlpt = obj["jlpt"]
    
  #checkslists
  resList = checkLists([obj["meanings"],obj["kun_readings"],obj["on_readings"],obj["name_readings"]])
  #write to a pyton dic called kanjiData 


  kanjiData = {
    "kanji" : obj["kanji"],
    "grade" : grade,
    "stroke_count"  : obj["stroke_count"],
    "meanings"  : resList[0],
    "heisig_en"  : heisig_en,
    "kun_readings" : resList[1],
    "on_readings" : resList[2],
    "name_readings" : resList[3],
    "jlpt"  : jlpt,
    "unicode" : obj["unicode"]  
    }
  return kanjiData

#gets data for a certain reading

def get_kanji_reading_data(reading):
  api_reading_link = "https://kanjiapi.dev/v1/reading/"
  urlReading = kanji_to_utf8_ascii_url_string(reading)

  try:
    with urllib.request.urlopen(api_reading_link + urlReading) as res:
      response = res.read()
  except urllib.error.HTTPError as exception:
    print(exception)
    return 404
  #decode response into utf-8 and then load json as a python obj
  decoded_response = response.decode("utf-8")
  obj = json.loads(decoded_response)


  resList = checkLists([obj["main_kanji"],obj["name_kanji"]])

  readingData = {
    "reading" : obj["reading"],
    "main_kanji" : resList[0],
    "name_kanji" : resList[1]
    }
  #print(readingData)
  return readingData

#gets dictionary data for a kanji

def get_kanji_word_data(word):
  #base api link
  api_word_link = "https://kanjiapi.dev/v1/words/"

  #gets knaji ready for url
  urlWord = kanji_to_utf8_ascii_url_string(word)


  #open link and get request
  #returns 404 if theres an HTTP Error
  try:
    with urllib.request.urlopen(api_word_link + urlWord) as res:
      response = res.read()
  except urllib.error.HTTPError as exception:
    print(exception)
    return 404

  #decode response into utf-8 and then load json as a python obj
  decoded_response = response.decode("utf-8")
  obj = json.loads(decoded_response)

  #######################################
  #way API calls work for wors
  # obj[i]["variants"][0]["written"]
  #   A       B         C     D
  # A = Which group, which comes in pairs of varients and meanings
  # B = Varients or meanings in the group
  # C = index of the VARIENT, which will have three cats, written, pronounced and priorities
  # D = Which one of the triad sub group. 
  
  # res[0]["meanings"][0]["glosses"])
  # ^^
  # from the wordData list
  #######################################

  #word data list were each index is a dictionary
  #where varients is all its varients, followed by its meanings
  wordData = []

  for i in range(0,len(obj)):
    indvWordData = {
      "variants" : obj[i]["variants"],
      "meanings" : obj[i]["meanings"]
      }
    wordData.append(indvWordData)
  return wordData

def get_kanji_list_data(list):
  #base api 
  api_list_link = "https://kanjiapi.dev/v1/kanji/"

  #make sure its a string
  grade=str(list)

  #open link and get request
  #returns 404 if theres an HTTP Error
  try:
    with urllib.request.urlopen(api_list_link + list) as res:
      response = res.read()
  except urllib.error.HTTPError as exception:
    print(exception)
    return 404

  #decode response into utf-8 and then load json as a python obj
  decoded_response = response.decode("utf-8")
  obj = json.loads(decoded_response)
  listData = obj
  return listData
