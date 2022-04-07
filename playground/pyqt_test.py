# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\gui\template\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5.QtCore import QRect, QMetaObject, QCoreApplication
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QListView, QTextBrowser, QMenuBar, QStatusBar, QMenu, QAction


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        self.setObjectName("MainWindow")
        self.resize(771, 386)

        self.centralwidget = QWidget()
        self.centralwidget.setObjectName("centralwidget")

        self.listView = QListView(self.centralwidget)
        self.listView.setGeometry(QRect(40, 40, 291, 231))
        self.listView.setObjectName("listView")

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QRect(40, 280, 91, 31))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QRect(140, 280, 91, 31))
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QRect(240, 280, 91, 31))
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QRect(360, 130, 81, 31))
        self.pushButton_4.setObjectName("pushButton_4")

        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QRect(470, 80, 231, 131))
        self.textBrowser.setObjectName("textBrowser")

        self.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar()
        self.menubar.setGeometry(QRect(0, 0, 771, 21))
        self.menubar.setObjectName("menubar")

        self.menuSpeech_Transcriber = QMenu(self.menubar)
        self.menuSpeech_Transcriber.setObjectName("menuSpeech_Transcriber")

        self.setMenuBar(self.menubar)
        self.statusbar = QStatusBar()
        self.statusbar.setObjectName("statusbar")

        self.setStatusBar(self.statusbar)
        self.actionFile = QAction()
        self.actionFile.setObjectName("actionFile")

        self.menuSpeech_Transcriber.addAction(self.actionFile)
        self.menubar.addAction(self.menuSpeech_Transcriber.menuAction())

        self.retranslateUI()
        QMetaObject.connectSlotsByName(self)

    def retranslateUI(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Record"))
        self.pushButton_2.setText(_translate("MainWindow", "Play"))
        self.pushButton_2.clicked.connect(self.playAudio)
        self.pushButton_3.setText(_translate("MainWindow", "Delete"))
        self.pushButton_4.setText(_translate("MainWindow", "Transcribe"))
        self.menuSpeech_Transcriber.setTitle(_translate("MainWindow", "File"))
        self.actionFile.setText(_translate("MainWindow", "Import API Key"))

    def playAudio(self):
        print("playAudio")

    def append_to_list(self, recording):
        self.listView.addItem(recording)

    # def keyPressEvent(self, event):
    #     if event.key() == Qt.Key_Escape:
    #         self.close()


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.initializeUI()
    ui.show()
    sys.exit(app.exec_())
