import sys
from hashlib import sha1
from HTMLParser import HTMLParser

isMac = sys.platform.startswith("darwin")
isWin = sys.platform.startswith("win32")
isLin = not isMac and not isWin

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def stripHTML(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def getList(dict):
    dictList = list()
    for key, value in dict.iteritems():
        dictList.append(value)
    return dictList

def checksum(data):
    return sha1(data).hexdigest()

def fieldChecksum(data):
    # 32 bit unsigned number from first 8 digits of sha1 hash
    return int(checksum(data.encode("utf-8"))[:8], 16)