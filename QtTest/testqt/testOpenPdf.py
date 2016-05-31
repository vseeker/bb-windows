# -*- coding: utf-8 -*-

import sys,os
#获取脚本文件的当前路径
def cur_file_dir():
     #获取脚本路径
     path = sys.path[0]
     #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)
#打印结果
print cur_file_dir()
os.popen(r'"J:\Foxit Reader\FoxitReader.exe" J:\py\bb-master\QtTest\testqt\1.pdf') # 由于windows平台利用shell命令打开pdf
# 文档的命令是用单引号强制引用的，而不是双引号，所以不能格式化，解决思路：由于你每次只点击一个按钮
# 所以生成一个固定名字的pdf然后打开是可以完成目标的，另外采取格式化生成.py脚本的方式，里面只有os.popen()函数，修改里面的pdf文件名即可
# 然后同样利用shell 命令，python xx.py的方式打开