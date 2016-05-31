# -*- coding:utf-8 -*-

import sys
from PySide import QtGui, QtCore

class queryResultWidget(QtGui.QWidget):

    def __init__(self):
        super(queryResultWidget, self).__init__()

        self.initUI()

    def initUI(self):
        self.queryBtnList = []
        self.myGroupBox = queryResultWidget()
        self.myGroupBox.setGeometry(QtCore.QRect(30, 420, 921, 200))

    def showDynamicButton(self, queryInfo):
        # queryInfo 匹配度（匹配关键词穿关键词）
        self.btnLength = 80
        self.btnWidth = 60
        # self.buttonCounter = int(raw_input("please input the button numbers:"))
        for el in xrange(len(queryInfo)):
            num = el + 1
            self.queryBtnList.append(QtGui.QPushButton(self.myGroupBox))
            self.queryBtnList[el].setGeometry(QtCore.QRect(self.btnLength, self.btnWidth * num, 113, 32))
            self.queryBtnList[el].setObjectName("pushButton{0}".format(el))
            self.queryBtnList[el].setText(
                QtGui.QApplication.translate("MainWindow", "{0}{1}".format(num, queryInfo[el]), None,
                                             QtGui.QApplication.UnicodeUTF8))
            self.queryBtnList[el].clicked.connect(self.buttonClicked)
            self.queryBtnList[el].show()
            # print self.queryBtnList
    def buttonClicked(self): # 定义槽函数

        sender = self.sender()
        print sender.text()
        self.statusBar().showMessage(sender.text() + ' was pressed')

def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()