import socket


class SocketClient:
    def __init__(self, ip, port) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server = ip, port

    def send_to(self, data: dict) -> None:
        self.sock.sendto(data, self.server)

    def close(self):
        self.sock.close
