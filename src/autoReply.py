from time import sleep, localtime, strftime
import os
import keyboard
import threading
from pywinauto.application import Application
from pywinauto.keyboard import SendKeys

from creative.somme import FearGamesChatSum


continua = True
tag_timeout = True


class FearGaemsChatTag(FearGamesChatSum):
    def __init__(self, game):
        super(FearGaemsChatTag, self).__init__(game, MAX_TIMEOUT=4)
        self.__i = 0
        self.__game = game
        self.words = ["Sto AFK, se ti servo scrivimi su Telegram", "Hek off", "I sAiD hEeEk OoOf",
                      "Sto qui per buildare e per i token ehehe", "<.< Sto dormendo", "40 Token per lo script l-:"]

    def sendChat(self, text="[Error] sum error"):
        self.__game.type_keys(text, with_spaces=True)
        sleep(0.2)
        self.__game.type_keys("{ENTER}")
        sleep(0.5)
        keyboard.send("t")

    def sendTag(self):
        print(strftime("%H:%M:%S", localtime()), "Risposta in chat")
        self.sendChat(f"[Messaggio automatico] {self.words[self.__i]}")
        self.__i = ((self.__i+1) % len(self.words))


def stopFile(key):
    global continua
    continua = False


def timeout_tag():
    global tag_timeout
    tag_timeout = True


def main(Chat):
    global continua, tag_timeout
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
                if "alessandrobasi §8»" not in line and "@alessandrobasi" in line:
                    if tag_timeout:
                        Chat.sendTag()
                        tag_timeout = False
                        threading.Timer(15, timeout_tag).start()
                elif "GIOCO > Risolvi" in line:
                    Chat.sendSum(line)


if __name__ == "__main__":
    app = Application().connect(
        title_re="Minecraft.*")
    game = app.window(class_name="GLFW30")
    Chat = FearGaemsChatTag(game)
    main(Chat)
