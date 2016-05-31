# -*- coding: utf-8 -*-
import os
import sys
import datetime
import time
from bosonnlp import BosonNLP

myApiToken = "X0njNWj2.5612.pYnhvqV02Kgn"
nlp = BosonNLP(myApiToken)
for eachLine in open("simple.txt"):
    # print eachLine,type(eachLine)
    # break
    # print nlp.extract_keywords(eachLine)
    result = nlp.tag(eachLine)
    print result
# print nlp.sentiment("这家味道还不错")
# print nlp.extract_keywords("instructor.txt")
