from threading import Thread

from src import web_server
from src.socket_server import SocketServer
from configs import services


def main() -> None:
    socket_server = SocketServer(services.UDP_IP,
                                 services.UDP_PORT)

    web = Thread(target=web_server.run,
                 args=[services.WEB_IP, services.WEB_PORT])
    web.start()

    socket_server.run()


if __name__ == "__main__":
    main()
