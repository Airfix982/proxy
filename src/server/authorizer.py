import socket
import json
import hashlib

from src.server.http_parser import parseHttp, parseLoginPwd


def checkWhiteIp(path, ip):
    with open(path, "r") as file:
        whiteIps = json.load(file)
        return False if ip in whiteIps["whiteIps"] else True

def checkIfBanned(src, dst, config):

    isSrcBanned = checkWhiteIp(config["SRC_WHITE_IPS"], src)
    isDstBanned = checkWhiteIp(config["DST_WHITE_IPS"], dst)
    return isSrcBanned, isDstBanned
    
def authorize(conn, srcIp, config, login, pwdHash):
    if login is None or pwdHash is None:
        requestAuthorization(conn, srcIp)
    if checkAuth(login, pwdHash, config["PROXY_PASSWORD_HASH"], config["PROXY_LOGIN"]):
        print("auth succ")
        return True
    else:
        print("auth fail")
        return False


def checkAuth(login, password, origin_password, origin_login): # rewrite
    return login == origin_login and password == origin_password
    
def requestAuthorization(conn: socket.socket, srcIp): # move into handler logic of talking with host
    #requests to auth
    try:
        conn.sendall(
            b"HTTP/1.1 407 Proxy Authentication Required\r\n"
            b"Proxy-Authenticate: Basic realm=\"MyProxy\"\r\n"
            b"Content-Length: 24\r\n"
            b"Connection: close\r\n"
            b"\r\n"
            b"Authentication required"
        )
    except TypeError as e:
        print(e)
    except OSError as e:
        print(e)
        pass




