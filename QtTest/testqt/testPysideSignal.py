# -*- coding: utf-8 -*-
from PySide import QtCore
import logManager
import speech_recognition as sr

btnTurnFlag = True
class audioRecognition(QtCore.QObject):
    signalAudioRecognized = QtCore.Signal(str)
    def __init__(self):
        self.r = sr.Recognizer()
        super(audioRecognition, self).__init__()
        self.signalAudioRecognized.connect(self.showEmit)
        try:
            self.signalAudioRecognized.emit("hello world")
        except Exception as e:
            print("__init__:")
            print(e)
    def showEmit(self,string):
        print string


    def audioRecognition(self):
        global btnTurnFlag
        while btnTurnFlag:
            logManager.logRecord(moduleDescription="audioRecognition come in ", logPath="audioRecognition.log",
                                 logLevel=1)

            with sr.Microphone() as source:
                # 监听一秒钟用于设定相关阈值
                self.r.adjust_for_ambient_noise(
                    source)  # listen for 1 second to calibrate the energy threshold for ambient noise levels
                self.signalAudioRecognized.emit("Say something!")
                self.signalAudioRecognized.emit("hi yai")
                audio = self.r.listen(source)

            try:
                self.signalAudioRecognized.emit("trying to recognize ... ")
                self.signalAudioRecognized.emit("Google Speech Recognition results:")
                resultTmp = self.r.recognize_google(audio,show_all=True)
                if not len(resultTmp):  # 识别结果为空，因为输入的声音很小或者没有输入
                    self.signalAudioRecognized.emit('声音太小或者没有声音')
                    continue
                else:
                    counter = 0
                # print resultTmp[u'alternative']
                # print resultTmp, type(resultTmp)
                for el in resultTmp[u'alternative']:
                    for ell in el:
                        counter += 1
                        if ell == 'confidence':  # 可信度
                            self.signalAudioRecognized.emit("{0},{1}".format(ell, el[ell]))
                        else:
                            self.signalAudioRecognized.emit("{0}".format(el[ell]))

            except sr.UnknownValueError:
                self.signalAudioRecognized.emit("Google Speech Recognition could not understand audio")

            except sr.RequestError as e:
                self.signalAudioRecognized.emit("Could not request results from Google Speech Recognition service; {0}".format(e))


t = audioRecognition()
t.audioRecognition()