import random
from selenium import webdriver
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import copy
import keyboard

def loadDict(file):
    f = open(file, 'r')
    data = f.read().split('\n')
    output = []
    for d in data:
        output.append(d.upper())
    f.close()    
    
    return output

def allInDict(d, syllable):
    output = []
    for word in d:
        if syllable.upper() in word:
            output.append(word)
    
    return output

def findBest(d, syllable, prefer, exclude):
    bestWord = ''
    score = -1
    usedLetters = []
    for word in d:
        if word in exclude:
            continue

        if syllable.upper() in word:
            # get score
            currentScore = 0
            letters = []
            for req in prefer:
                if req.upper() in word:
                    currentScore += 1
                    letters.append(req.upper())
            
            if currentScore > score:
                score = currentScore
                bestWord = word
                usedLetters = letters
        
    return bestWord, usedLetters

letterTemplate = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L' 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
currentRemainingLetters = copy.deepcopy(letterTemplate)

allWords = loadDict('dict.txt')
commonWords = loadDict('20k.txt')

browser = webdriver.Firefox()
browser.get('https://jklm.fun')

hasSwitched = False

wordsUsed = []

queuedWord = ''

while (True):
    if not hasSwitched:
        try:
            browser.switch_to.frame(0)
            hasSwitched = True
        except:
            continue
    
    if keyboard.is_pressed('f1'):
        otherTurn = browser.find_elements(By.CLASS_NAME, 'selfTurn')
        if len(otherTurn) == 0:
            continue
        if otherTurn[0].get_attribute('hidden') == "":
            continue

        elements = browser.find_elements(By.CLASS_NAME, 'syllable')
        if len(elements) == 0:
            continue
        element = elements[0]
        syllable = element.get_attribute('innerText').upper()

        best, usedLetters = findBest(allWords, syllable, currentRemainingLetters, wordsUsed)
            
        wordsUsed.append(best)
        for letter in usedLetters:
            currentRemainingLetters.remove(letter)
        
        if len(currentRemainingLetters) == 0:
            currentRemainingLetters = copy.deepcopy(letterTemplate)
        
        print(best)
        
        queuedWord = best
        
        print('========')
        
        keyboard.write(queuedWord)
        keyboard.press_and_release('enter')