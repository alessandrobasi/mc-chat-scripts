from time import sleep, localtime, strftime
import os
import keyboard
import threading
import re
import random
from pywinauto.application import Application
from pywinauto.keyboard import SendKeys


continua = True
tag_timeout = True


class FearGaemsChatWinner():
    def __init__(self, game):
        self.__i = 0
        self.__game = game
        self.player = []

    def sendChat(self, text="[Error] error"):
        self.__game.type_keys(text, with_spaces=True)
        sleep(0.2)
        self.__game.type_keys("{ENTER}")
        sleep(0.5)
        keyboard.send("t")

    def addPlayer(self, line):
        chat = line.split(" ", maxsplit=4)[4]
        chat = re.sub(r"\§.", '', chat)[:-1]
        name, chat = chat.split("»")
        if name not in self.player:
            print("aggiunto:", name)
            self.player.append(name)

    def getWinner(self):
        print("scegliendo vincitore\n", self.player)
        if self.player != []:
            win = random.choice(self.player)
            print(win)
            return win


def stopFile(key=''):
    global continua, Chat
    continua = False


def timeout_tag():
    global tag_timeout
    tag_timeout = True


def main(Chat):
    global continua, tag_timeout
    keyboard.on_press_key(72, stopFile, suppress=False)

    path_logfile = os.path.join(
        os.getenv("APPDATA"), ".minecraft\\logs\\latest.log")

    Chat.sendChat(
        "Scrivete \"@alessandrobasi F\" per essere sorteggiati per vincere 10 token, Avete 1 minuto [F maiuscola]")
    threading.Timer(60, stopFile).start()

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
                if "alessandrobasi §8»" not in line and "@alessandrobasi F" in line:
                    Chat.addPlayer(line)
        Chat.sendChat(f"L'utente {Chat.getWinner()} ha vinto 10 token")


if __name__ == "__main__":
    app = Application().connect(
        title_re="Minecraft.*")
    game = app.window(class_name="GLFW30")
    Chat = FearGaemsChatWinner(game)
    main(Chat)
