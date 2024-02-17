import os
from time import sleep
from utils.controller import *

if __name__ == "__main__": 
    os.system('stty -echo')
    controller = get_controller() 
    try:
        while True:
            try:
                c_input = controller.read()
                print(c_input)
            except OSError:
                controller = get_controller()
    except KeyboardInterrupt:
        print("Closing")
        os.system("stty echo")
