from time import sleep, localtime, strftime
import os
import keyboard
from pywinauto.application import Application
from pywinauto.keyboard import SendKeys

continua = True


class FearGamesChatSum:
    def __init__(self, game,MAX_TIMEOUT=3):

        self.MAX_TIMEOUT = MAX_TIMEOUT
        self.__timeout = self.MAX_TIMEOUT

        self.__game = game

    def sendChat(self, text="[Error] sum error"):
        self.__game.type_keys(text, with_spaces=True)
        sleep(0.2)
        self.__game.type_keys("{ENTER}")
        sleep(0.5)
        keyboard.send("t")

    def sendSum(self, line):
        chat = line.split(" ", maxsplit=4)[4]
        result = eval(chat[16:-74])
        if self.__timeout == 0:
            self.sendChat(result)
        print(strftime("%H:%M:%S", localtime()), chat[16:-75], "=", result, "| Timeout =",self.__timeout)
        self.__timeout = ((self.__timeout-1) % self.MAX_TIMEOUT)


def stopFile(key):
    global continua
    continua = False


def main(Chat):
    global continua
    keyboard.on_press_key(72, stopFile, suppress=False)

    path_logfile = os.path.join(
        os.getenv("APPDATA"), ".minecraft\\logs\\latest.log")
    with open(path_logfile, "r", encoding="ANSI") as logfile:
        logfile.readlines()
        while continua:
            where = logfile.tell()
            line = logfile.readline()
            if not line:
                sleep(1)
                logfile.seek(where)
            else:
                # print(line),  # already has newline
                if "GIOCO > Risolvi" in line:
                    Chat.sendSum(line)
                    game.minimize()


if __name__ == "__main__":
    app = Application().connect(
        title_re="Minecraft.*")
    game = app.window(class_name="GLFW30")
    Chat = FearGamesChatSum(game)
    main(Chat)
