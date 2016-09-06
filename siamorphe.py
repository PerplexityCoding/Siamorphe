# -*- coding: utf-8 -*-

import json
import logging
import click
import sys

from core.service.SiamorpheService import SiamorpheService
from PyQt4 import QtCore, QtGui, QtWebKit

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

class Browser(QtGui.QMainWindow):

    def __init__(self):
        """
            Initialize the browser GUI and connect the events
        """

        QtGui.QMainWindow.__init__(self)
        self.resize(800,600)
        self.centralwidget = QtGui.QWidget(self)

        self.mainLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.mainLayout.setSpacing(0)
        self.mainLayout.setMargin(1)

        self.frame = QtGui.QFrame(self.centralwidget)

        self.gridLayout = QtGui.QVBoxLayout(self.frame)
        self.gridLayout.setMargin(0)
        self.gridLayout.setSpacing(0)

        self.html = QtWebKit.QWebView()
        self.gridLayout.addWidget(self.html)
        self.mainLayout.addWidget(self.frame)
        self.setCentralWidget(self.centralwidget)

        self.default_url = "https://google.fr"
        self.browse()

    def browse(self):
        """
            Make a web browse on a specific url and show the page on the
            Webview widget.
        """

        url = self.default_url
        self.html.load(QtCore.QUrl(url))
        self.html.show()

@click.command()
@click.option("--gui", default=False, help="launch the gui", is_flag=True)
def command(gui):

    if gui:
        # launch socket server
        logging.debug("launch the gui")

        app = QtGui.QApplication(sys.argv)
        main = Browser()
        main.show()
        sys.exit(app.exec_())

        # open the browser

    else:
        notes = """ [{"id": 1, "expression": "日本語が大好きです", "level": 70},
                     {"id": 2, "expression": "私が日本語を勉強しました", "level": 30},
                     {"id": 3, "expression": "日本語の学校が第一", "level": 0}
                     ] """

        siamorpheService = SiamorpheService("jp")
        #siamorpheService.analyzeNotes(notes)
        siamorpheService.analyzeNotesFile('C://Users//yves_menard//Perso//Workspace//Siamorphe//sample//notes2.csv')

if __name__ == '__main__':
    command()