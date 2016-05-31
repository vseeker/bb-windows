# -*- coding: utf-8 -*-
import os
import sys
import datetime
import time


def localIpFilter():
    buff = []
    for ln in open('stop.txt'):
        if ln in buff:
            continue
        buff.append(ln)
    with open('stopWords.txt', 'w+') as handle:
        handle.writelines(buff)
start = time.clock()
localIpFilter()
end = time.clock()
print end-start