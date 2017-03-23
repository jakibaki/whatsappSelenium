#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import sys
import os
from time import sleep, ctime
from _thread import start_new_thread
import requests
from random import randint

def FindWhenNameExists(name, web):
    timeout = 150
    element_present = EC.presence_of_element_located((By.CLASS_NAME, name))
    WebDriverWait(web, timeout).until(element_present)
    return web.find_element_by_class_name(name)



def init(path):
    
    if(not os.path.isfile(path)):
        print("get your secrets using https://github.com/Mawalu/whatsapp-phishing and put the 'secrets' file in the current Folder.")
        exit(0)


    virtualDisplay = True
    if sys.platform == 'linux2':
        try:
            if(virtualDisplay):
                from pyvirtualdisplay import Display
                display = Display(visible=0, size=(800, 600))
                display.start()
        except ImportError:
            print("VirtualDisplay is enabled but not installed!\nFalling back to normal mode!")

    web = webdriver.Chrome()
    web.get("https://web.whatsapp.com")
    file = open(path)
    web.execute_script("var t = " + file.read() + 
                       "\nfunction login(token) {Object.keys(token.s).forEach(function (key) {localStorage.setItem(key, token.s[key])}); token.c = token.c.split(';'); token.c.forEach(function(cookie) {document.cookie = cookie; });}" +
                       "\nlogin(t)")
    file.close()
    web.get("https://web.whatsapp.com")
    FindWhenNameExists('input',web) #waits until it finished loading
    return web

def goto(text,web):
    web.find_element_by_xpath('//span[contains(text(),"' + text + '")]').click()



def send(text,web):
    text = text.split("\n")
    input = web.find_elements_by_class_name('input')[1]

    actions = ActionChains(web)
    actions.move_to_element(input)

    for i in text:
        actions.send_keys(i).key_down(Keys.SHIFT).send_keys("\n").key_up(Keys.SHIFT)
        print(i)
        print(text)
    actions.send_keys("\n").perform() #this \n is without shift so it actually sends the message

def getLatestMsg(web):
    #A bit hacky but it works (I was getting seemingly random errors when switching the current contact)
    try:
        input_box = web.find_element(By.XPATH, '//*[@id="side"]//input')
        input_box.clear()
        input_box.click()
        input_box.send_keys(Keys.RETURN)


        msg = web.find_elements_by_class_name('bubble-text')
        msg = msg[len(msg)-1]
        msg = msg.find_elements_by_class_name('message-text')[0]
        id = msg.get_attribute('data-id')
        msg = msg.text
        return([msg,id,"true" in id])
    except:
        return(["","",True])

num = 0
zahlenRaten = False
step = 0
def messageHandler(web,msg):
    global zahlenRaten
    global num
    global step
    if(msg[0].startswith('!') and not msg[2]):
        if(msg[0].lower().startswith('!help')):
            send('Liste aller Befehle:\n' + 
                 '*!help* zeigt diese Seite\n' +
                 '*!zeit* gibt die aktuelle Uhrzeit und das aktuelle Datum aus\n' +
                 '*!zahlenraten* startet/stoppt ein Zahlen-rate-Spiel', web)
        elif(msg[0].lower().startswith('!zeit')):
            send('Es ist: ' + ctime(), web)
        elif(msg[0].lower().startswith('!zahlenraten')):
            if(not zahlenRaten):
                send('Startet ein neues Zahlen-rate-Spiel mit zahlen von 1 bis 100...\n' +
                     'Gib *!n _nummer_* ein um eine Zahl zu raten!', web)
                zahlenRaten = True
                num = randint(1,100)
                step = 0
            else:
                send('Stoppe das aktuelle Zahlen-rate-Spiel!', web)
        elif(msg[0].lower().startswith('!n ')):
            if(zahlenRaten):
                guessNum = int(msg[0][3:])
                if(guessNum <= 100 and guessNum >= 1):
                    step += 1
                    if(guessNum>num):
                        send('Deine Zahl ist zu Groß', web)
                    elif(guessNum<num):
                        send('Deine Zahl ist zu Klein', web)
                    elif(guessNum == num):
                        send('Deine Zahl ist richtig!\n' +
                             'Du hast die Zahl in ' + str(step) + ' Schritten gefunden!', web)
                        zahlenRaten = False
                else:
                    send('Du hast keine Zahl zwischen 1 und 100 eingegeben!', web)
            else:
                send('Es Läuft momentan kein Zahlen-rate-Spiel!\n' +
                     'Starte eins mit *!zahlenraten*.', web)
        else:
            send('Das ist kein valider Befehl.\n' + 
                 'Nutze *!help* um Hilfe zu bekommen!', web)
    print(msg)

def messageLoop(web):
    last = getLatestMsg(web)[1]
    while True:
        msg = getLatestMsg(web)
        if(last != msg[1]):
            messageHandler(web,msg)
        
        last = msg[1]
        sleep(0.5)


web = init("secrets")
print("Successfully logged in!")


#gotoLatest(web)

start_new_thread(messageLoop, (web, ))

input("Press return to exit!\n")

web.quit()