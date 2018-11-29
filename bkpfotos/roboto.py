import pyautogui
import time
import os


class Coordenates():
    menuBtn = (25,1058)
    terminalBtn = (25, 280)
    chromeBtn = (25, 50)
    chromeNewTabBtn = (1850,73)
    chromeAdressBarr = (907,109)

def pressMenu():
    print("press Menu")
    pyautogui.click(Coordenates.menuBtn)
    pyautogui.moveTo(200, 200)

def pressMenu():
    print("press Menu")
    pyautogui.click(Coordenates.menuBtn)

def pressEnter():
    pyautogui.typewrite(['enter'])

def pressF11():
    pyautogui.typewrite(['f11'])

def typeText(text, delay):
    time.sleep(delay)
    pyautogui.typewrite(text)

def openTerminal():
    pyautogui.click(Coordenates.terminalBtn)

def openChrome():
    pyautogui.click(Coordenates.chromeBtn)

def click(coordenates):
    pyautogui.click(coordenates)

def showMovies():
    openChrome()
    click(Coordenates.chromeNewTabBtn)
    click(Coordenates.chromeAdressBarr)
    typeText('http://m4ufree.live/top-movies', 0.1)
    pressEnter()
    pressF11()

def commitProject():
    openTerminal()
    
    typeText('git add .; git commit -m "Commit"; git push -u origin master; xmessage "Feito Carreto!";', 0.0001)
    pressEnter()
    typeText('cristianzortea@gmail.com', 3)
    pressEnter()
    typeText('CRjava24', 2)
    pressEnter()

print("press Menu")

#pressMenu()
#commitProject()

showMovies()




