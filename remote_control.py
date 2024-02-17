import os
from time import sleep
import signal
from utils.controller import *

if __name__ == "__main__": 
    os.system('stty -echo')
    controller = get_controller() 
    try:
def signal_handler(sig, frame):
    print("Closing...")
    os.system('stty echo')
    exit(0)

signal.signal(signal.SIGINT, signal_handler)
        while True:
            try:
                c_input = controller.read()
                print(c_input)
            except OSError:
                controller = get_controller()
