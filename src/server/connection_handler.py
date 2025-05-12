import socket

from src.server.http_parser import parseHttp
from src.server.authorizer import checkIfBanned, authorize, authFailed
from src.server.tunnel import setConnection
from src.server.transfer import transferData

def handleConnection(connection, address, config):
    dstDomain, dstPort, method, protocol, login, pwdHash = parseHttp(connection)
    if method == b'CONNECT':
        dstIp = getIpByDomain(dstDomain)
        srcIp, srcPort = address
        if not handleAuth(connection, srcIp, dstIp, config, login, pwdHash):
            return
        dstSock = setConnection(dstIp, int(dstPort))
        noteHost(connection, srcIp)
        transferData(connection, dstSock)
    else:
        handleBadMethod(connection)
        return


    
def handleBadMethod(conn):
    conn.sendall(
        b"HTTP/1.1 405 Method Not Allowed\r\n\r\n"
    )
    conn.close()
    return


def noteHost(conn, ip):
    try:
        conn.sendall(
            b"HTTP/1.1 200 Connection Established\r\n\r\n"
        )
    except:
        pass


def handleAuth(conn, srcIp, dstIp, config, login, pwdHash):
    isSrcBanned, isDstBanned = checkIfBanned(srcIp, dstIp, config)
    if isSrcBanned:
        bannedIp(conn, srcIp)
        return False
    elif isDstBanned:
        bannedIp(conn, dstIp)
        return False
    if not authorize(conn, srcIp, config, login, pwdHash):
        authFailed(conn)
        return False
    return True

def bannedIp(conn: socket.socket, ip):
    try:
        conn.sendall(
            b"HTTP/1.1 401 Forbidden\r\n"
            b"Content-Type: text/plain\r\n"
            b"Connection: close\r\n"
            b"\r\n"
        )
        conn.close()
    except OSError as e:
        pass
    # conn.send(bytes(f'IP {ip} is not in whute list. Bad luck', encoding='utf-8'))



def getIpByDomain(hostname):
    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except:
        pass