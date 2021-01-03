import eel
import random
import string
import time
import os
import sys

eel.init('backend')

class HangmanHandler():
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

    for item in range(len(list(word))):
        full_word.append("_")

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

    handler_img[1] = img
    handler_img[0] = handler

@eel.expose()
def startWin():
    eel.flwRain()

@eel.expose()
def restart():
    handler_img[1] =0
    reset()
    eel.reload()
try:
    eel.start('main.html')
except:
    pass
