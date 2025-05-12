import socket as socket
import threading
from socket import AF_INET, SOCK_STREAM

from src.server.http_parser import parseHttp
from src.server.connection_handler import handleConnection


def listenNewConnection(address: str, port: int, config):
    with socket.socket(family=AF_INET, type=SOCK_STREAM) as sock:
        sock.bind((address, port))
        maxConnections = 20
        while True:
            sock.listen(maxConnections)
            conn, addr = sock.accept()
            thread = threading.Thread(target=handleConnection, kwargs={'connection': conn, 'address': addr, 'config': config})
            thread.start()


def main(config):
    address = '0.0.0.0'
    port = 8888
    connetction = listenNewConnection(address, port, config)


if __name__ == "__main__":
    main()