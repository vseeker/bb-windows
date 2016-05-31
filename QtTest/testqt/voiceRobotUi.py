# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'voiceRobot.ui'
# Created: Tue Apr 26 15:37:50 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
# WARNING! All changes made in this file will be lost!
# from PySide import QtCore, QtGui
# from PySide import QtWebKit
import queryData
import os
from PySide import *
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
from sys import byteorder
from array import array
from struct import pack
from recorder import *
import pyaudio
import wave
import time
import threading
import audioRecordControl
import logManager
import speech_recognition as sr
import PyBaiduYuyin as pby
btnTurnFlag = False
chineseFlag = False
englishFlag = False
global keyWordList
keyWordList = ['机器人', '控制器', '电源']

# audio recognition
class audioRecognition(QtCore.QObject):
    global btnTurnFlag, chineseFlag, englishFlag
    signalAudioRecognized = QtCore.Signal(str)
    def __init__(self):
        self.r = sr.Recognizer()
        super(audioRecognition, self).__init__()
        # self.signalAudioRecognized.connect(self.showEmit)
        # try:
        #     self.signalAudioRecognized.emit("hello world")
        # except Exception as e:
        #     print("__init__:")
        #     print(e)
    # def showEmit(self,string):
    #     print string

    def chineseAudioRecognition(self):
        global btnTurnFlag, chineseFlag
        global englishFlag # 测试button点击信号切换正确后，删除englishFlag
        print "进入线程", btnTurnFlag
        while True:
            time.sleep(1)
            while btnTurnFlag and chineseFlag:
                print "中文识别while里面主线程：{0}，中文识别：{1}，英文识别{2}".format(btnTurnFlag,chineseFlag,englishFlag)

                # obtain audio from the microphone
                r = pby.Recognizer()
                with pby.Microphone() as source:
                    # 监听一秒钟用于设定相关阈值
                    r.adjust_for_ambient_noise(
                        source)  # listen for 1 second to calibrate the energy threshold for ambient noise levels
                    self.signalAudioRecognized.emit(u"说点什么")
                    audio = r.listen(source)

                # for testing purposes, we're just using the default API key
                self.signalAudioRecognized.emit(u"正在尝试识别")
                # self.signalAudioRecognized.emit(u"识别结果是:")
                resultTmp = r.recognize(audio)
                # print "识别结果{0}的字符格式为{1}".format(resultTmp,type(resultTmp))
                if resultTmp is None: # 由于修改了源码(这里跳过异常报错，修改为发生任何识别错误都会返回None)，直接进行下次识别
                    print "识别为空"
                    continue
                else:
                    self.signalAudioRecognized.emit(u"{0}".format(resultTmp))


    def audioRecognition(self):
        global btnTurnFlag, englishFlag
        global chineseFlag #  测试button点击信号切换正确后，删除chineseFlag
        print "进入线程",btnTurnFlag
        while True:
            time.sleep(1)
            while btnTurnFlag and englishFlag:
                print "英文识别while里面主线程：{0}，中文识别：{1}，英文识别{2}".format(btnTurnFlag,chineseFlag,englishFlag)
                logManager.logRecord(moduleDescription="audioRecognition come in ", logPath="audioRecognition.log",
                                     logLevel=1)

                with sr.Microphone() as source:
                    # 监听一秒钟用于设定相关阈值
                    self.r.adjust_for_ambient_noise(
                        source)  # listen for 1 second to calibrate the energy threshold for ambient noise levels
                    # self.signalAudioRecognized.emit("Say something!")
                    audio = self.r.listen(source)

                try:
                    # self.signalAudioRecognized.emit("trying to recognize ... ")
                    # self.signalAudioRecognized.emit("Google Speech Recognition results:")
                    resultTmp = self.r.recognize_google(audio,show_all=True)
                    if not len(resultTmp):  # 识别结果为空，因为输入的声音很小或者没有输入
                        self.signalAudioRecognized.emit('声音太小或者没有声音')
                        # print "声音太小或者没有声音"
                        continue
                    else:
                        counter = 0
                    # print "已识别"
                    # print resultTmp[u'alternative']
                    # print resultTmp, type(resultTmp)
                    for el in resultTmp[u'alternative']:
                        for ell in el:
                            counter += 1
                            if ell == 'confidence':  # 可信度
                                self.signalAudioRecognized.emit("{0},{1}".format(ell, el[ell]))
                            elif counter<3:
                                self.signalAudioRecognized.emit("{0}".format(el[ell]))

                except sr.UnknownValueError:
                    self.signalAudioRecognized.emit("Google Speech Recognition could not understand audio")

                except sr.RequestError as e:
                    self.signalAudioRecognized.emit("Could not request results from Google Speech Recognition service; {0}".format(e))


# audio wave data prepare

SR = SwhRecorder()
SR.setup()
SR.continuousStart()
time.sleep(5)

# audio Section definition




def threadAudioRecord( ):
    global btnTurnFlag
    logManager.logRecord( moduleDescription="thread AudioRecord  Begin and the btnTurnFlag is:{0} ".format(btnTurnFlag), logLevel=1 )

    while True :
        if not btnTurnFlag:
            logManager.logRecord( moduleDescription="the btnTurnFlag is:{0}".format(btnTurnFlag), logLevel=1 )
            time.sleep(2)
            continue
        logManager.logRecord(moduleDescription=" record begin and the btnTurnFlag is:{0}".format(btnTurnFlag), logLevel=1 )
        p = pyaudio.PyAudio( )
        CHUNK_SIZE = 2048  # 修改这里以控制语音文件的大小，4096大概10s太大了
        FORMAT = pyaudio.paInt16
        RATE = 44100
        stream = p.open( format=FORMAT, channels=1, rate=RATE,
                         input=True, output=True,
                         frames_per_buffer=CHUNK_SIZE ) # 这里的采集音频数据的类型要和下面存储的时候保持一致比如通道数

        num_silent = 0
        snd_started = False

        r = array( 'h' )

        while True :
            # little endian, signed short
            snd_data = array( 'h', stream.read( CHUNK_SIZE ) )
            if byteorder == 'big':
                snd_data.byteswap( )
            r.extend( snd_data )

            silent = audioRecordControl.is_silent( snd_data )

            if silent and snd_started:
                num_silent += 1
            elif not silent and not snd_started:
                snd_started = True

            if snd_started and num_silent > 20 or not btnTurnFlag: # num_silent 20 对应3-4s
                break

        logManager.logRecord(moduleDescription="break out while and btnTurnFlag now is {0}".format(btnTurnFlag),logLevel=1)
        sample_width = p.get_sample_size( FORMAT )
        stream.stop_stream( )
        stream.close( )
        p.terminate( )

        r = audioRecordControl.normalize( r )
        r = audioRecordControl.trim( r )
        r = audioRecordControl.add_silence( r, 0.5 )
        data = r
        # return sample_width, data
        path = str( int( time.time( ) ) ) + '.wav'
        # print btnTurnFlag, path
        data = pack( '<' + ('h' * len( data )), *data )

        wf = wave.open( path, 'wb' )
        wf.setnchannels( 1 )
        wf.setsampwidth( sample_width )
        wf.setframerate( RATE )
        wf.writeframes( data )
        wf.close( )
        logManager.logRecord(moduleDescription="audio have recorded as {0}".format(path),logLevel=1)


class queryResultWidget(QtGui.QWidget):

    def __init__(self):
        super(queryResultWidget, self).__init__()
        self.initUI()
        self.dictQueryResult = {}
        # queryInfo 匹配度（匹配关键词穿关键词）
        self.btnLength = 150
        self.btnWidth = 32

    def initUI(self):
        # self.myGroupBox = QtGui.QWidget()
        self.setGeometry(QtCore.QRect(30, 420, 921, 200))

    def showDynamicButton(self, queryInfo): #根据queryInfo中的关键字（经停用词过滤后的关键字），用按钮显示这些关键词
        # 当点击按钮时，显示对应的pdf，遗留问题：由于字符的长度不定，目前按钮的大小是固定的，所以有可能会造成显示不完整的情况
        self.queryBtnList = []

        l = 0 #横向偏移 （0-5个单位长度）
        h = 0 #纵向偏移（0-n个单位长度）
        # self.buttonCounter = int(raw_input("please input the button numbers:"))
        for el in xrange(len(queryInfo)): # 可以改成enumerate的形式
            num = el
            self.queryBtnList.append(QtGui.QPushButton(self))
            if num % 5 : #横向延伸
                l = num % 5
                self.queryBtnList[el].setGeometry(QtCore.QRect(self.btnLength*l+20, self.btnWidth*h+20, self.btnLength, self.btnWidth ))
            else: #纵向
                l = num % 5
                h = num / 5
                self.queryBtnList[el].setGeometry(QtCore.QRect(self.btnLength*l+20, self.btnWidth * h+20, self.btnLength, self.btnWidth))

            self.queryBtnList[el].setObjectName("pushButton{0}".format(el))
            self.queryBtnList[el].setText(
                QtGui.QApplication.translate("MainWindow", "{0}{1}".format(num, queryInfo[el]), None,
                                             QtGui.QApplication.UnicodeUTF8))
            self.queryBtnList[el].clicked.connect(self.buttonClicked)
            self.queryBtnList[el].show()
            # print self.queryBtnList
    def showQueryResult(self): # 将数据库查询结果显示出来，并且通过点击按钮（或声控）打开对应pdf文件
        global keyWordList
        queryInfo = []
        keyWordList = queryData.filterStopWord(keyWordList)
        self.dictQueryResult =  queryData.mergeResult(queryData.mergeQueryResult(keyWordList))
        for k in self.dictQueryResult.iterkeys():
            queryInfo.append(k)
        self.showDynamicButton(queryInfo)

    def buttonClicked(self): # 定义槽函数,点击那个键，即显示对应的pdf

        sender = self.sender()
        pdfId = int(sender.text()[:1]) # 该数也即字典中用于合成pdf的数据所在字典中的位置

        print 'buttonId',pdfId
        threadShowQueryDBInfo = threading.Thread( target=self.showQueryDBInfo,args=(pdfId,) )
        threadShowQueryDBInfo.start()
        # for index , tup in enumerate(self.dictQueryResult.items()):
        #     if index == pdfId: # tup即（关键词串，[pageId...]）
        #         queryData.showPdfWhenButtonClicked(tup,1)#pdf名固定为1.pdf
        #         os.popen(r'"J:\Foxit Reader\FoxitReader.exe" J:\py\bb-master\QtTest\testqt\1.pdf')
                # self.statusBar().showMessage(sender.text() + ' was pressed')

    def showQueryDBInfo(self,pdfId):
        for index, tup in enumerate(self.dictQueryResult.items()):
            if index == pdfId:  # tup即（关键词串，[pageId...]）
                queryData.showPdfWhenButtonClicked(tup, 1)  # pdf名固定为1.pdf
                os.popen(r'"J:\Foxit Reader\FoxitReader.exe" J:\py\bb-master\QtTest\testqt\1.pdf')



class VoiceRobotUI(object):
    global btnTurnFlag, SR,englishFlag,chineseFlag
    global queryInfo


    def showAudioRecognitionResult(self, string):
        # print string
        self.speakResult.append(string)



    def waveUpdate(self):
        self.curve.setData(SR.audio.flatten())

    def setupUi(self, Form):
        self.queryBtnList = []
        Form.setObjectName("Form")
        Form.resize(1366, 768)

        self.pushButton = QtGui.QPushButton(Form)
        # self.pushButton.setGeometry(QtCore.QRect(440, 650, 75, 41))
        self.pushButton.setGeometry(QtCore.QRect(1000, 300, 75, 41))

        self.pushButton.setObjectName("pushButton")
        self.pushButton.setIcon(QtGui.QIcon("stop.png"))
        self.pushButton.clicked.connect( self.buttonClicked )

        self.btn_language = QtGui.QPushButton(Form)
        # self.btn_language.setGeometry(QtCore.QRect(190, 650, 75, 41))
        self.btn_language.setGeometry(QtCore.QRect(1000, 400, 75, 41))

        self.btn_language.setObjectName("languageButton")
        self.btn_language.setIcon(QtGui.QIcon("stop.png"))
        self.btn_language.clicked.connect(self.buttonLanguageClicked)



        self.speakResult = QtGui.QTextBrowser(Form)
        self.speakResult.setGeometry(QtCore.QRect(30, 60, 421, 281))
        self.speakResult.setObjectName("speakResult")
        # self.speakResult.setText("hello world")
        # self.speakResult.append("hi")

        # show audio wave
        self.voiceWave = pg.PlotWidget(Form)
        self.voiceWave.setGeometry(QtCore.QRect(500, 60, 421, 281))
        self.voiceWave.setObjectName("voiceWave")
        self.curve = self.voiceWave.plot()
        self.curve.setPen((200, 200, 100))
        self.curve.setData(SR.audio.flatten())
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.waveUpdate)
        self.timer.start(5)  # 控制刷新频率

        # 显示语音识别的结果
        self.audioRecognition = audioRecognition()

        self.audioRecognition.signalAudioRecognized.connect(self.showAudioRecognitionResult)
        # self.audioRecognition.signalAudioRecognized.emit("hello")

        # 显示数据库查询的结果
        self.qureyBox = queryResultWidget()
        self.scroll = QtGui.QScrollArea(Form)
        self.scroll.setWidget(self.qureyBox)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(300)
        self.scroll.setGeometry(QtCore.QRect(30, 420, 891, 200))

        self.qureyBox.showQueryResult()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # 录音线程
        # threadAudioControl = threading.Thread( target=threadAudioRecord )
        # threadAudioControl.start()

        # 实时英文识别线程
        threadAudioRecognition = threading.Thread( target= self.audioRecognition.audioRecognition )
        threadAudioRecognition.start()
        # 实时中文识别线程
        threadChineseAudioRecognition = threading.Thread(target=self.audioRecognition.chineseAudioRecognition)
        threadChineseAudioRecognition.start()


    def buttonLanguageClicked(self):
        global chineseFlag, englishFlag, btnTurnFlag
        if btnTurnFlag: # 确认主线程启动,只有主线程启动的时候，切换才有意义，此时可以进行语言识别的切换
            if chineseFlag: # 当前是识别中文，则切换为识别英文

                chineseFlag = False
                englishFlag = True
                self.btn_language.setText(
                    QtGui.QApplication.translate("Form", "English", None, QtGui.QApplication.UnicodeUTF8))

                print "切换为识别英文主线程：{0}，中文识别：{1}，英文识别{2}".format(btnTurnFlag,chineseFlag,englishFlag)
            else: # 当前是识别英文，切换为识别中文
                englishFlag = False
                chineseFlag = True
                self.btn_language.setText(
                    QtGui.QApplication.translate("Form", "Chinese", None, QtGui.QApplication.UnicodeUTF8))
                print "切换为识别中文主线程：{0}，中文识别：{1}，英文识别{2}".format(btnTurnFlag,chineseFlag,englishFlag)
        else:
            print "主线程play键未点击，识别线程未开启主线程：{0}，中文识别：{1}，英文识别{2}".format(btnTurnFlag,chineseFlag,englishFlag)


    def buttonClicked(self):
        global btnTurnFlag,chineseFlag,englishFlag

        if btnTurnFlag:
            chineseFlag = False
            englishFlag = False
            self.pushButton.setIcon( QtGui.QIcon( "stop.png" ) )
            btnTurnFlag = False
            print "buttonClicked主线程：{0}，中文识别：{1}，英文识别{2}".format(btnTurnFlag,chineseFlag,englishFlag)
        else:
            chineseFlag = True
            self.pushButton.setIcon( QtGui.QIcon( "play.png" ) )
            btnTurnFlag = True
            print "buttonClicked主线程：{0}，中文识别：{1}，英文识别{2}".format(btnTurnFlag, chineseFlag, englishFlag)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_language.setText(QtGui.QApplication.translate("Form", "Chinese", None, QtGui.QApplication.UnicodeUTF8))


