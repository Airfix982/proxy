import select
import socket

def transferData(srcConn: socket.socket, dstConn: socket.socket):
    while True:
        read_sockets, _, _ = select.select([srcConn, dstConn], [], [])
        for sock in read_sockets:
            data = sock.recv(4096)
            if not data:
                return
            if sock == srcConn:
                dstConn.send(data)
            else:
                srcConn.send(data)
