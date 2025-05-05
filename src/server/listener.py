import socket as socket
import threading
from socket import AF_INET, SOCK_STREAM

from parser import parseHttp


def listenNewConnection(address: str, port: int, authkey: bytes):
    with socket.socket(family=AF_INET, type=SOCK_STREAM) as sock:
        sock.bind((address, port))
        maxConnections = 10
        while True:
            sock.listen(maxConnections)
            conn, addr = sock.accept()
            with conn:
                thread = threading.Thread(target=parseHttp, kwargs={'connection': conn, 'address': addr})
                thread.start()


if __name__ == "__main__":
    address = '0.0.0.0'
    port = 8888
    connetction = listenNewConnection(address, port)