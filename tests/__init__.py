

import socket
from PyFileShare import share_directory

from threading import Thread
import pyautogui
from time import sleep

def end():
    sleep(10)
    input("Press ENTER to exit")
    return

if __name__ == '__main__':
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    Thread(target=end).start()
    share_directory("../src/", host=str(host_ip))
    ...
