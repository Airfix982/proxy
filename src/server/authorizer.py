import socket
import json
import hashlib

from src.server.http_parser import parseHttp, parseLoginPwd


def checkBlackIp(path, ip):
    with open(path, "r") as file:
        blackIps = json.load(file)
        return True if ip in blackIps["blackIps"] else False

def checkIfBanned(src, dst, config):

    isSrcBanned = checkBlackIp(config["SRC_BLACK_IPS"], src)
    isDstBanned = checkBlackIp(config["DST_BLACK_IPS"], dst)
    return isSrcBanned, isDstBanned
    
def authorize(conn, srcIp, config, login, pwdHash):
    if login is None or pwdHash is None:
        requestAuthorization(conn, srcIp)
    if checkAuth(login, pwdHash, config["PROXY_PASSWORD_HASH"], config["PROXY_LOGIN"]):
        return True
    else:
        return False


def checkAuth(login, password, origin_password, origin_login):
    return login == origin_login and password == origin_password
    
def requestAuthorization(conn: socket.socket): 
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
        pass
    except OSError as e:
        pass



def authFailed(conn):
    try:
        conn.sendall(
            b"HTTP/1.1 401 Authentication Required\r\n"
            b"Proxy-Authenticate: Basic realm=\"MyProxy\"\r\n"
            b"Content-Length: 0\r\n"
            b"Connection: close\r\n"
            b"\r\n"
        )
    except OSError as e:
        pass
