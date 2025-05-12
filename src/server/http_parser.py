import socket
import base64
import hashlib

def parseHttp(connection: socket.socket):
    try:
        header = connection.recv(4096)
        headerParts = header.split()
        method = headerParts[0]
        dst = headerParts[1]
        protocol = headerParts[2]
        login = None
        password = None
        try:
            proxyAuthIndex = headerParts.index(b'Basic')
            authBase64 = headerParts[proxyAuthIndex + 1]
            login, password = getAuthParamsFromBase64(authBase64)
            if not password is None:
                password = hashlib.sha256(password.encode()).hexdigest()
            pass
        except ValueError as e:
            #print(e)
            pass

        dstParts = (dst.decode('utf-8')).split(':')
        dstDomain, dstPort = dstParts[0], dstParts[1]
        return dstDomain, dstPort, method,  protocol, login, password

    except OSError or TypeError as e:
        pass

def getAuthParamsFromBase64(base64str: bytes):
    try:
        originalBytes = base64.b64decode(base64str)
        originString = originalBytes.decode('utf-8')
        stringParts = originString.split(':')
        return stringParts[0], stringParts[1]
    except ValueError or TypeError as e:
        pass

def parseLoginPwd(conn): # move into parser
    try:
        authData = ((conn.recv(1024)).decode('utf-8')).split()
        login, pwd = authData[0], authData[1]
        return login, pwd
    except:
        pass
    