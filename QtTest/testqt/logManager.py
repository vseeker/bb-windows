# coding=utf-8
import logging
import os


def logRecord(moduleDescription="test123", logPath="./log/audioRecord.log", logLevel=3): # 相对路径,./指上一级,
                                                                                            # ../指上上一级
    # type: (str, str, int) -> None
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M', filename=logPath, filemode='a+')
    thisLog = logging.getLogger(moduleDescription)
    logLevelList = ['debug', 'info', 'warning', 'error']
    logLevelDict = {'debug': lambda: thisLog.debug(' '), 'info': lambda: thisLog.info(' '),
                    'warning': lambda: thisLog.warning('warning!, please check it'),
                    'error': lambda: thisLog.error('error!,u should check it immediately')}
    logLevelDict.get(logLevelList[logLevel])()


def logManager(logPath="test.log", size=50):
    #  "size = 50" means if the size of log > 50MB ,then it will be cleaned
    if os.path.exists(logPath):
        fileSize = os.path.getsize(logPath)
        # print fileSize
        limitSize = size * 1048576
        if limitSize < fileSize:
            os.remove(logPath)
            logRecord(moduleDiscription="logManager just refreshed the dnsLog", logLevel=1)

# logRecord(moduleDescription="hello world",logLevel=1)