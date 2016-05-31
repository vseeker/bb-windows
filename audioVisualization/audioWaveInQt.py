# -*- coding: utf-8 -*-

from recorder import *
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import time
import sys


def update():
    global curve, pw
    curve.setData(SR.audio.flatten())

SR = SwhRecorder()
SR.setup()
SR.continuousStart()
time.sleep(5)
app = QtGui.QApplication([])
mw = QtGui.QMainWindow()  # 主窗口
mw.setWindowTitle('audio Plotting')  # 窗口名
mw.resize(800, 600)  # 设定窗口大小
cw = QtGui.QWidget()  # 初始化一个顶层工具类
mw.setCentralWidget(cw)  # 将该工具居中
l = QtGui.QVBoxLayout()  # 初始化一个布局类
cw.setLayout(l)  # 在主窗口中设置该布局

pw = pg.PlotWidget(name='audio Plotting')  # 创建一个画图小工具
l.addWidget(pw, 0)  # 将该工具添加到布局中

# btn = QtGui.QPushButton("press me")
# l.addWidget(btn, 1)

mw.show()  # 显示主窗口
curve = pw.plot()  # 创建一个空的Curve
curve.setPen((200, 200, 100))
curve.setData(SR.audio.flatten())

timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(5)  # 控制刷新频率


if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
    QtGui.QApplication.instance().exec_()
    SR.close()
    SR.continuousEnd()



