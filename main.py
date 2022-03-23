
from PySide2 import QtCore, QtGui
import sys
from PySide2.QtCore import QEventLoop, QTimer
from PySide2.QtWidgets import QApplication, QMainWindow
from Ui_main import Ui_MainWindow
import os
from PySide2.QtCore import Slot


class EmittingStr(QtCore.QObject):
   textWritten = QtCore.Signal(str)  # 定义一个发送str的信号，这里用的方法名与PyQt5不一样

   def write(self, text):
       self.textWritten.emit(str(text))
       loop = QEventLoop()
       QTimer.singleShot(1000, loop.quit)
       loop.exec_()

class ControlBoard(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(ControlBoard, self).__init__()
        self.setupUi(self)
        # 下面将输出重定向到textEdit中
        sys.stdout = EmittingStr()
        self.textEdit.connect(sys.stdout, QtCore.SIGNAL("textWritten(QString)"), self.outputWritten)
        sys.stderr = EmittingStr()
        self.textEdit.connect(sys.stderr, QtCore.SIGNAL("textWritten(QString)"), self.outputWritten)
        self.pushButton.clicked.connect(self.bClicked)

    @Slot()	
    def outputWritten(self, text):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.textEdit.setTextCursor(cursor)
        self.textEdit.ensureCursorVisible()

    def execCmd(self,cmd):
      r = os.popen(cmd)
      text = r.read()
      r.close()
      return text

    def bClicked(self):
        print(self.execCmd("ls"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ControlBoard()
    win.show()
    sys.exit(app.exec_())