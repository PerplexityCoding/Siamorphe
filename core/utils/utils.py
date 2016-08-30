import sys
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