import os
from dotenv import load_dotenv
from pathlib import Path
import sys

from src.server.listener import main

# temporary solution
BASE_PATH = Path(__file__).resolve().parent
CONFIG_DIR = BASE_PATH / 'src' / 'config'

envPath = BASE_PATH / '.env'

SRC_BLACK_IPS = CONFIG_DIR / 'srcBlackIps.json'
DST_BLACK_IPS = CONFIG_DIR / 'dstBlackIps.json'
PROXY_LOGIN="proxy"
PROXY_PASSWORD_HASH="79f06f8fde333461739f220090a23cb2a79f6d714bee100d0e4b4af249294619"
#
load_dotenv()

#SRC_WHITE_IPS = #os.getenv("SRC_WHITE_IPS")
#DST_WHITE_IPS = #os.getenv("DST_WHITE_IPS")
config = {
    "SRC_BLACK_IPS" : SRC_BLACK_IPS,
    "DST_BLACK_IPS" : DST_BLACK_IPS,
    "PROXY_LOGIN" : PROXY_LOGIN,
    "PROXY_PASSWORD_HASH" : PROXY_PASSWORD_HASH
}

main(config)

