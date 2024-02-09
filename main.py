import os
import sys

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the root directory by going up one level from the script directory
project_root = os.path.dirname(os.path.dirname(script_path))

sys.path.insert(0, project_root)
sys.path.insert(0, os.getcwd())  # Add the current directory as well

from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QVBoxLayout, QSplitter, QWidget, QLabel, \
    QPlainTextEdit, QSizePolicy
from PyQt5.QtCore import Qt, QCoreApplication, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from apiWidget import ApiWidget
from mdiApp import MdiArea
from script import GPTJsonWrapper, load_and_instantiate_class

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)  # HighDPI support

QApplication.setFont(QFont('Arial', 12))


class Thread(QThread):
    generatedFinished = pyqtSignal(str)

    def __init__(self, wrapper, text):
        super(Thread, self).__init__()
        self.__wrapper = wrapper
        self.__text = text

    def run(self):
        try:
            self.generatedFinished.emit(self.__wrapper.get_data(self.__text))
        except Exception as e:
            raise Exception(e)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.__initVal()
        self.__initUi()

    def __initVal(self):
        self.__wrapper = GPTJsonWrapper()

    def __initUi(self):
        self.setWindowTitle('GPT PyQt GUI generator')

        lbl = QLabel('Prompt')
        self.__promptTextEdit = QPlainTextEdit()

        lay = QVBoxLayout()
        lay.addWidget(lbl)
        lay.addWidget(self.__promptTextEdit)

        leftWidget = QWidget()
        leftWidget.setLayout(lay)

        lbl = QLabel('Result')
        self.__resultMdiArea = MdiArea()

        lay = QVBoxLayout()
        lay.addWidget(lbl)
        lay.addWidget(self.__resultMdiArea)

        rightWidget = QWidget()
        rightWidget.setLayout(lay)

        self.__splitter = QSplitter()
        self.__splitter.addWidget(leftWidget)
        self.__splitter.addWidget(rightWidget)
        self.__splitter.setHandleWidth(1)
        self.__splitter.setChildrenCollapsible(False)
        self.__splitter.setSizes([300, 700])
        self.__splitter.setStyleSheet(
            "QSplitterHandle {background-color: lightgray;}")
        self.__splitter.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)

        self.__btn = QPushButton('Run')
        self.__btn.clicked.connect(self.__run)

        apiWidget = ApiWidget()

        lay = QVBoxLayout()
        lay.addWidget(apiWidget)
        lay.addWidget(self.__splitter)
        lay.addWidget(self.__btn)

        mainWidget = QWidget()
        mainWidget.setLayout(lay)

        self.setCentralWidget(mainWidget)

        apiWidget.aiEnabled.connect(self.__aiEnabled)

        f = apiWidget.isAiEnabled()
        self.__splitter.setEnabled(f)
        if f:
            self.__wrapper.set_api(apiWidget.getApiKey())

    def __aiEnabled(self, f, api_key):
        self.__splitter.setEnabled(f)
        if f:
            self.__wrapper = GPTJsonWrapper(api_key=api_key)
        else:
            self.__wrapper = GPTJsonWrapper(api_key=api_key)
        self.__wrapper.set_api(api_key)

    def __run(self):
        text = self.__promptTextEdit.toPlainText()

        self.__t = Thread(self.__wrapper, text)
        self.__t.started.connect(self.__started)
        self.__t.generatedFinished.connect(self.__generatedFinished)
        self.__t.finished.connect(self.__finished)
        self.__t.start()

    def __started(self):
        self.__btn.setEnabled(False)
        self.__resultMdiArea.clearSubWindow()

    def __generatedFinished(self, result):
        result_class = load_and_instantiate_class(result)
        self.__resultMdiArea.createSubWindow(result_class)

    def __finished(self):
        self.__btn.setEnabled(True)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())