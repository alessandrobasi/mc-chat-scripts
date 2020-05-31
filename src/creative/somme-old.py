from time import sleep, localtime, strftime
import os
import keyboard
from pyperclip import copy


def stopFile(key):
    global continua
    continua = False


def main():
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
                    chat = line.split(" ", maxsplit=4)[4]
                    print(strftime("%H:%M:%S", localtime()),
                          chat[16:-75], "=", eval(chat[16:-74]))
                    copy(eval(chat[16:-74]))


def testkey(key):
    print(key.scan_code)


continua = True


if __name__ == "__main__":
    # keyboard.hook(testkey)
    # sleep(100)
    main()
