# -*- coding: utf-8 -*-

from recorder import *
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import time
import sys


SR = SwhRecorder()
SR.setup()
SR.continuousStart()
time.sleep(5)
app = QtGui.QApplication([])
win = pg.GraphicsWindow(title="Basic plotting examples")
win.setWindowTitle('pyqtgraph example: Plotting')
pg.setConfigOptions(antialias=True)
p = win.addPlot(title="audio plot")
p.enableAutoRange('xy', True)
curve = p.plot(pen='y')


def update():
    global curve, p
    curve.setData(SR.audio.flatten())


def showAudioWave():
    global curve, p
    curve.setData(SR.audio.flatten())
    timer = QtCore.QTimer()
    timer.timeout.connect(update)
    timer.start(5)  # 控制刷新频率

    # SR.close() #运行的时候不要关掉，否则会没有数据导致界面卡住,要学会断点调试
    # SR.continuousEnd()
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
        SR.close()
        SR.continuousEnd()


showAudioWave()
