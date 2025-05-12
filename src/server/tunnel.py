import socket
from socket import AF_INET, SOCK_STREAM

def setConnection(dstIp, dstPort):
    try:
        sock = socket.socket(family=AF_INET, type=SOCK_STREAM)
        sock.connect((dstIp, dstPort))
        return sock
    except:
        pass


# dstIp = "18.185.192.125"
# dstPort = 443
# sock = setConnection(dstIp, dstPort)
# print(sock.fileno())