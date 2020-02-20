# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\python\Raspoznavanie_obj\Hakaton2part\Front.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
import sys
import image


class Ui_MainWindow(object):
    def setupUi(self, BoxDetection):
        BoxDetection.setObjectName("BoxDetection")
        BoxDetection.resize(411, 551)
        BoxDetection.setWindowTitle('Icon')
        BoxDetection.setWindowIcon(QIcon('icone.png')) 
        font = QtGui.QFont()
        font.setFamily("Rockwell")
        font.setPointSize(26)
        fon=QtGui.QFont()
        fon.setFamily("Rockwell")
        fon.setPointSize(13)
        font.setUnderline(True)
        BoxDetection.setFont(font)
        BoxDetection.setFont(fon)
        BoxDetection.setAutoFillBackground(False)
        
        self.label = QtWidgets.QLabel(BoxDetection)
        self.label.setFont(fon)
        self.label.setGeometry(QtCore.QRect(15, 10, 100, 20))
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(BoxDetection)
        self.label_2.setFont(fon)
        self.label_2.setGeometry(QtCore.QRect(7, 60, 100, 13))
        self.label_2.setObjectName("label_2")
		
        self.textEdit = QtWidgets.QTextEdit(BoxDetection)
        self.textEdit.setGeometry(QtCore.QRect(10, 30, 150, 25))
        self.textEdit.setStyleSheet("color: rgb(0, 0, 0);\n""background-image: url(:/pole/1.bmp);")
        self.textEdit.setObjectName("textEdit")
		
        self.textEdit_2 = QtWidgets.QTextEdit(BoxDetection)
        self.textEdit_2.setGeometry(QtCore.QRect(10, 75, 150, 25))
        self.textEdit_2.setStyleSheet("color: rgb(0, 0, 0);\n""background-image: url(:/pole/1.bmp);")
        self.textEdit_2.setObjectName("textEdit_2")
		
        BoxDetection.setStyleSheet("\n""background-image: url(:/fontan/z07xrBpJScI1.jpg);")
        self.pushButton = QtWidgets.QPushButton(BoxDetection)
        self.pushButton.setGeometry(QtCore.QRect(60, 140, 131, 41))
        self.pushButton.setMinimumSize(QtCore.QSize(131, 41))
        self.pushButton.setMaximumSize(QtCore.QSize(131, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bodoni MT")
        font.setPointSize(18)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background-color: rgb(149, 107, 214);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(BoxDetection)
        self.pushButton_2.setGeometry(QtCore.QRect(220, 140, 131, 41))
        self.pushButton_2.setMinimumSize(QtCore.QSize(131, 41))
        self.pushButton_2.setMaximumSize(QtCore.QSize(131, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bodoni MT")
        font.setPointSize(18)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("background-color: rgb(149, 107, 214);\n"
"")
        self.pushButton_2.setObjectName("pushButton_2")
        self.Selecting = QtWidgets.QLabel(BoxDetection)
        self.Selecting.setGeometry(QtCore.QRect(120, 100, 241, 31))
        self.Selecting.setMinimumSize(QtCore.QSize(241, 31))
        self.Selecting.setMaximumSize(QtCore.QSize(241, 16777215))
        font = QtGui.QFont()
        font.setFamily("Copperplate Gothic Light")
        font.setPointSize(18)
        font.setUnderline(False)
        self.Selecting.setFont(font)
        self.Selecting.setObjectName("Selecting")
        
        self.pushButton_3 = QtWidgets.QPushButton(BoxDetection)
        self.pushButton_3.setGeometry(QtCore.QRect(150, 420, 111, 41))
        self.pushButton_3.setMinimumSize(QtCore.QSize(111, 41))
        self.pushButton_3.setMaximumSize(QtCore.QSize(111, 16777215))
        font = QtGui.QFont()
        font.setFamily("Bodoni MT")
        font.setPointSize(18)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet("background-color: rgb(244, 110, 143) no-repeat;")
        self.pushButton_3.setObjectName("pushButton_3")
        
        self.pushButton_4 = QtWidgets.QPushButton(BoxDetection)
        self.pushButton_4.setGeometry(QtCore.QRect(60, 200, 40, 40))
        self.pushButton_4.setMinimumSize(QtCore.QSize(40, 40))
        self.pushButton_4.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButton_4.setFont(font)
        self.pushButton_4.setStyleSheet("background-image: url(:/fontan/BoxFall.jpg) no-repeat;")
        self.pushButton_4.setObjectName("pushButton_4")
        
        self.pushButton_5 = QtWidgets.QPushButton(BoxDetection)
        self.pushButton_5.setGeometry(QtCore.QRect(120, 200, 40, 40))
        self.pushButton_5.setMinimumSize(QtCore.QSize(40, 40))
        self.pushButton_5.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButton_5.setFont(font)
        self.pushButton_5.setStyleSheet("background-image: url(:/fontan/BoxOpen.jpg) no-repeat;")
        self.pushButton_5.setObjectName("pushButton_5")
        
        self.pushButton_6 = QtWidgets.QPushButton(BoxDetection)
        self.pushButton_6.setGeometry(QtCore.QRect(185.5, 200, 40, 40))
        self.pushButton_6.setMinimumSize(QtCore.QSize(40, 40))
        self.pushButton_6.setMaximumSize(QtCore.QSize(40, 16.777215))
        self.pushButton_6.setFont(font)
        self.pushButton_6.setStyleSheet("background-image: url(:/fontan/Clock.jpg) no-repeat;")
        self.pushButton_6.setObjectName("pushButton_6")
        
        self.pushButton_7 = QtWidgets.QPushButton(BoxDetection)
        self.pushButton_7.setGeometry(QtCore.QRect(251, 200, 40, 40))
        self.pushButton_7.setMinimumSize(QtCore.QSize(40, 40))
        self.pushButton_7.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButton_7.setFont(font)
        self.pushButton_7.setStyleSheet("background-image: url(:/fontan/BoxRoy.jpg) no-repeat;")
        self.pushButton_7.setObjectName("pushButton_7")
        
        self.pushButton_8 = QtWidgets.QPushButton(BoxDetection)
        self.pushButton_8.setGeometry(QtCore.QRect(311, 200, 40, 40))
        self.pushButton_8.setMinimumSize(QtCore.QSize(40, 40))
        self.pushButton_8.setMaximumSize(QtCore.QSize(40, 16777215))
        self.pushButton_8.setFont(font)
        self.pushButton_8.setStyleSheet( "background-image: url(:/fontan/Some.jpg) no-repeat; ")
        self.pushButton_8.setObjectName("pushButton_8")

        self.textBrowser = QtWidgets.QTextBrowser(BoxDetection)
        self.textBrowser.setGeometry(QtCore.QRect(70, 250, 271, 141))
        self.textBrowser.setMinimumSize(QtCore.QSize(271, 141))
        self.textBrowser.setMaximumSize(QtCore.QSize(271, 16777215))
        self.textBrowser.setStyleSheet("color: rgb(0, 0, 0);\n""background-image: url(:/pole/1.bmp);")
        self.textBrowser.setObjectName("textBrowser")
        self.IBM = QtWidgets.QLabel(BoxDetection)
        self.IBM.setGeometry(QtCore.QRect(300, 10, 101, 71))
        self.IBM.setMinimumSize(QtCore.QSize(101, 71))
        self.IBM.setMaximumSize(QtCore.QSize(101, 16777215))
        self.IBM.setText("")
        self.IBM.setPixmap(QtGui.QPixmap(":/IBM/ibm.png"))
        self.IBM.setObjectName("IBM")

        self.retranslateUi(BoxDetection)
        QtCore.QMetaObject.connectSlotsByName(BoxDetection)

    def retranslateUi(self, BoxDetection):
        _translate = QtCore.QCoreApplication.translate
        BoxDetection.setWindowTitle(_translate("BoxDetection", "BoxDetection"))
        self.pushButton.setText(_translate("BoxDetection", "Video"))
        self.pushButton_2.setText(_translate("BoxDetection", "Web"))
        self.Selecting.setText(_translate("BoxDetection", "Select mode:"))
        self.pushButton_3.setText(_translate("BoxDetection", "Exit"))
        self.label.setText(_translate("BoxDetection", "Login"))
        self.label_2.setText(_translate("BoxDetection", "  Password"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_MainWindow()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

