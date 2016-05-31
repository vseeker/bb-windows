# -*- coding: utf-8 -*-

import sys
from PySide.QtCore import *
from PySide.QtGui import *
from voiceRobotUi import VoiceRobotUI


class GoToCellDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        self.ui = VoiceRobotUI()
        self.ui.setupUi(self)


def main():
    app = QApplication(sys.argv)
    d = GoToCellDialog()
    d.show()
    # d.showFullScreen()
    sys.exit(app.exec_())
    SR.close()
    SR.continuousEnd()

if __name__ == '__main__':
    main()