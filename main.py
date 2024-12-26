import os
import sys

from rutube import Rutube

from PyQt5 import QtCore, QtGui, QtWidgets
from untitled import *


class downloader(QtCore.QThread):
    mysignal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.url = None

    def run(self):
        self.mysignal.emit('Процесс скачивания запущен!')

        video = Rutube(self.url)
        video.get_best().download()

        self.mysignal.emit('Процесс скачивания завершен!')
        self.mysignal.emit('Finish!')

    def init_args(self, url):
        self.url = url


class gui(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.downloader_folder = None
        self.ui.Vibor_papki.clicked.connect(self.get_folder)
        self.ui.load.clicked.connect(self.start)
        self.mythread = downloader()
        self.mythread.mysignal.connect(self.handler)

    def start(self):
        if len(self.ui.lineEdit.text())>5:
            if self.downloader_folder != None:
                link = self.ui.lineEdit.text()
                self.mythread.init_args(link)
                self.mythread.start()
                self.locker(True)
            else:
                QtWidgets.QMessageBox.warning(self, "Ошибка!", "Вы не выбрали папку!")
        else:
            QtWidgets.QMessageBox.warning(self, "Ошибка!", "Ссылка на видео не указана")

    def get_folder(self):
        self.downloader_folder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Выбрать папку для сохранения')
        os.chdir(self.downloader_folder)

    def locker(self, lock_value):
        base = [self.ui.Vibor_papki, self.ui.load]
        for item in base:
            item.setDisabled(lock_value)

    def handler(self, value):
        if value == 'Finish!':
            self.locker(False)
        self.ui.plainTextEdit.appendPlainText(value)

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = gui()
    win.show()
    sys.exit(app.exec_())