from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

import eel
import random
import string
import time
import os
import sys

import pickle

import configparser
import requests

eel.init('backend')

str2dev = lambda data: transliterate(data, sanscript.HK, sanscript.DEVANAGARI)

def getglobs():
    x = pickle.load(open("glob.pkl", "rb"))
    return x
def setglobs(goal, q, dq, caq):
    open("glob.pkl", "wb").truncate()
    pickle.dump([goal, q, dq, caq], open("glob.pkl", "wb"))

class HangmanHandler():


    dq = 0

    cur = open("db.txt", "r")
    s = random.sample(cur.readlines(), 1)
    word = random.choice(s).lower().replace("\n", "").rstrip().split(":", 1)
    hint = word[1]
    word = word[0]

    hangman = 0
    uw = []
    w = string.ascii_lowercase
    full_word = []
    fw = []

    dev_word = str2dev(word)
    dev_fword = []
    dev_fw = []

    for item in range(len(list(word))):
        full_word.append("_")

    for item in range(len(list(dev_word))):
        dev_fword.append("_")

    def update_db(self, w):
        cur = open("db.txt", "w")
        print("Ok, now type the words, and i will save it in the database. Type QUIT to exit")
        while True:
            cur.write(w+"\n")

        cur.close()
    def play_game(self, guess):
        char = guess
        indecies = [i for i, x in enumerate(self.word) if x == char]

        if indecies != []:
            self.fw = list(self.full_word)
            for item in indecies:
                self.fw[item] = char

            self.full_word = "".join(str(v) for v in self.fw)

            if self.full_word == self.word:
                return "FULL"
            else:
                self.uw.append(char)
                return "HALF"
        else:
            self.uw.append(char)
            return "BAD"

    def smb_game(self, guess):
        char = guess
        indecies = [i for i, x in enumerate(self.dev_word) if x == char]

        if indecies != []:
            self.dev_fw = list(self.dev_fword)
            for item in indecies:
                self.fw[item] = char

            self.dev_fword = "".join(str(v) for v in self.fw)

            if self.dev_fword == self.dev_word:
                return "FULL"
            else:
                self.uw.append(char)
                return "HALF"
        else:
            self.uw.append(char)
            return "BAD"

global handler_img
handler_img = [HangmanHandler(), 0]

def reset():
    handler_img[0] = HangmanHandler()

'''
@eel.expose()
def start_game():
    handler = handler_img[0]
    eel.uiFinish()
    eel.txt_hint()
    eel.set_full_word("".join(str(v) + " " for v in handler.full_word))
    eel.set_txt_hint(handler.hint)
    handler_img[0] = handler

'''

@eel.expose()
def push():
    h = handler_img[0]
    burl = "https://RK3K3UG6BXQM6ZIF.anvil.app/_/private_api/7RW34ZQIM63GI2AUA6WWADJI/update_leaderboard/"
    try:
        tok = configparser.ConfigParser()
        tok.read("config.ini")
        tok = tok["push"]["token"]
    except:
        eel.a("Invalid Token! Please Close The Brower To Exit")
        exit()
    else:
        burl += tok
        burl += "/" + str(h.dq)

        requests.get(burl)

        eel.a("You can close the Browser-window")
        exit()

@eel.expose()
def fwrite(tk):
    with open("config.ini", "w") as f:
        f.write(f"""
[push]
token={tk}
        """)

@eel.expose()
def start_game():
    handler = handler_img[0]
    if "http" in handler.hint or "images/" in handler.hint:
        eel.img_hint()
        eel.set_full_word("".join(str(v) + " " for v in handler.full_word))
        eel.set_pic_hint(handler.hint)

    else:
        eel.txt_hint()
        eel.set_full_word("".join(str(v) + " " for v in handler.full_word))
        eel.set_txt_hint(handler.hint)

    eel.uiFinish()
    eel.kpec()


@eel.expose()
def keypress(key):
    handler = handler_img[0]
    img = handler_img[1]
    res = handler.play_game(key.lower())
    eel.set_full_word("".join(str(v) + " " for v in list(handler.full_word)))
    if res == "BAD":
        base_url = "https://raw.githubusercontent.com/simonjsuh/Vanilla-Javascript-Hangman-Game/master/images/{}.jpg"
        if img == 6:

            eel.looseScreen()
            eel.init_page_l()

        else:
            eel.updateHangman(base_url.format(str(img + 1)))
            img += 1

    if res == "FULL":
        eel.winScreen()
        eel.init_page_w()

        handler.dq += 1

    handler_img[1] = img
    handler_img[0] = handler


@eel.expose()
def startWin():
    eel.flwRain()

@eel.expose()
def smbKeypress(key):
    handler = handler_img[0]
    img = handler_img[1]
    res = handler.smb_game(key.lower())
    eel.setDeva("".join(str(v) + " " for v in list(handler.dev_fword)))
    if res == "BAD":
        base_url = "https://raw.githubusercontent.com/simonjsuh/Vanilla-Javascript-Hangman-Game/master/images/{}.jpg"
        if img == 6:
            eel.looseScreen()
            eel.init_page_l()
        else:
            eel.updateHangman(base_url.format(str(img + 1)))
            img += 1

    if res == "FULL":
        eel.winScreen()
        eel.init_page_w()

    handler_img[1] = img
    handler_img[0] = handler

@eel.expose()
def set_full():
    eel.set_full_word_red(handler_img[0].word)

@eel.expose()
def restart():
    handler_img[1] =0
    reset()
    eel.reload()
@eel.expose()
def res():
    eel.reopen()
try:

    eel.start('main.html')
except:
    pass
