# -*- coding: utf-8 -*-
import os
import sys
import datetime
import time


def loadStopWord(filePath ="stopWords.txt" ):
    buff = []
    with open(filePath) as fp:
        for ln in fp:
            buff.append(ln)
    return buff
    print len(buff)

start = time.clock()
loadStopWord()
end = time.clock()
print end-start