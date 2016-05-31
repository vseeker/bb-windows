# -*- coding: utf-8 -*-
import PySide
from PySide.QtCore import *
from PySide.QtGui import *
import sys

# Create a Qt application
app = QApplication(sys.argv)
# Create a Label and show it
label = QLabel("Hello World")
label.show()
# Enter Qt application main loop
app.exec_()
sys.exit()