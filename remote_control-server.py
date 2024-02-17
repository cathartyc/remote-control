from argparse import ArgumentParser
from utils.input_data import INPUT_DATA
import signal
import socket

def signal_handler(sig, frame):
    print("Closing...")
    exit(0)

signal.signal(signal.SIGINT, signal_handler)

HOST = '0.0.0.0'
PORT = 1234

parser = ArgumentParser()
parser.add_argument(
    'port',
    metavar='PORT',
    type=int,
    default=PORT,
    nargs='?',
    help='the port the server should listen for'
)

args = parser.parse_args()
PORT = args.port

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as so:
        so.bind((HOST, PORT))
        print(f'Listening on {HOST}:{PORT}...')
        so.listen()
        connection, client = so.accept()
        with connection:
            print(f'Connection enstablished with {client}')
            while True:
                input = connection.recv(1)
                if not input:
                    break
                input = INPUT_DATA(int.from_bytes(input))
                print(f'Received {input} from {client}')
        print("Connection closed.")
