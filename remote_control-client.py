from argparse import ArgumentParser
import os
import signal
import socket
from time import sleep
from utils.controller import *

def signal_handler(sig, frame):
    print("Closing...")
    os.system('stty echo')
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

HOST = "127.0.0.1"
PORT = 1234

parser = ArgumentParser()
parser.add_argument(
    'host',
    metavar='HOST',
    type=str,
    default=HOST,
    nargs='?',
    help='the host of the server'
)
parser.add_argument(
    'port',
    metavar='PORT',
    type=int,
    default=PORT,
    nargs='?',
    help='the port the server should listen for'
)

args = parser.parse_args()
HOST = args.host
PORT = args.port


os.system('stty -echo')
controller = get_controller()
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as so:
        try:
            print(f'Connecting to {HOST}:{PORT}...')
            so.connect((HOST, PORT))
        except ConnectionRefusedError:
            print('Retrying in 3 seconds...')
            sleep(3)
            continue
        else:
            print(f'Connected to {HOST}:{PORT}!')
        while True:
            try:
                c_input = controller.read()
                so.sendall(c_input.value.to_bytes(1))
                print(f'Sent {c_input}')
            except OSError:
                controller = get_controller()
