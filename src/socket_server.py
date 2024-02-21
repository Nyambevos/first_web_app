import socket
import json
import urllib.parse
from datetime import datetime


class SocketServer:
    def __init__(self, ip, port) -> None:
        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM)
        self.server = ip, port

    def run(self) -> None:
        self.sock.bind(self.server)
        try:
            print('Start Socket Server')
            while True:
                data, address = self.sock.recvfrom(1024)
                data_parse = urllib.parse.unquote_plus(data.decode())
                data_dict = {key: value for key, value in
                             [el.split('=') for el in data_parse.split('&')]}
                print(f'Received data: {data_dict} from: {address}')
                self._save_data(data_dict)

        except KeyboardInterrupt:
            print('Destroy server')
        finally:
            self.sock.close()

    def _save_data(self, data) -> None:
        with open('storage/data.json', 'r') as file:
            data_file = json.load(file)
            data_file[f"{datetime.now()}"] = data
            with open('storage/data.json', 'w') as file:
                json.dump(data_file, file)
