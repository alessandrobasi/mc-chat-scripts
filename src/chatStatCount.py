# legge la chat e vede quanti msg al sec
# gli utenti con più chat
# eccc

from time import sleep, localtime, strftime
import os
import keyboard
import re
import threading
from pywinauto.application import Application
from pywinauto.keyboard import SendKeys


continua = True


class FearGaemsChatStat:
    def __init__(self, game, char):
        self.__game = game
        self.__char = char
        self.stat = dict()

    def sendChat(self, text="[Error] sum error"):
        self.__game.type_keys(text, with_spaces=True)
        sleep(0.2)
        self.__game.type_keys("{ENTER}")
        sleep(0.5)
        keyboard.send("t")

    def getChat(self, line):
        chat = line.split(" ", maxsplit=4)[4]
        chat = re.sub(r"\§.", '', chat)[:-1]
        name, chat = chat.split(self.__char)
        if self.stat.get(name):
            self.stat[name] += 1
        else:
            self.stat[name] = 1
        print(strftime("%H:%M:%S", localtime()), name, chat)

    def startTimer(self, time):
        self.__time = time
        threading.Timer(self.__time, lambda: stopFile(None)).start()

    def result(self):
        tot_msg = 0
        top_user = ""
        top_user_msg = 0
        for k, v in list(self.stat.items()):
            tot_msg += v
            if v > top_user_msg:
                top_user_msg = v
                top_user = k

        print("Messaggi inviati in", self.__time, ":", tot_msg,
              "\ntop user:", top_user, "msg:", top_user_msg)


def stopFile(key):
    global continua, Chat
    continua = False
    Chat.result()


def main(Chat, char):
    global continua
    keyboard.on_press_key(72, stopFile, suppress=False)

    path_logfile = os.path.join(
        os.getenv("APPDATA"), ".minecraft\\logs\\latest.log")

    with open(path_logfile, "r", encoding="ANSI") as logfile:
        logfile.readlines()  # Vai alla fine del file per il tell

        while continua:

            where = logfile.tell()
            line = logfile.readline()
            if not line:
                sleep(1)
                logfile.seek(where)
            else:
                # C'è un nuovo messaggio
                if char in line:
                    Chat.getChat(line)


if __name__ == "__main__":
    #  »
    app = Application().connect(
        title_re="Minecraft.*")
    game = app.window(class_name="GLFW30")
    char = input("Carattere di divisione msg: ")
    time = float(input("Tempo di monitoraggio: "))
    Chat = FearGaemsChatStat(game, char)
    if time != -1:
        Chat.startTimer(time)
    main(Chat, char)
