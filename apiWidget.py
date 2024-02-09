import requests
from PyQt5.QtCore import pyqtSignal, QSettings

from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QLineEdit, QLabel, QPushButton, QHBoxLayout, QWidget


class ApiWidget(QWidget):
    aiEnabled = pyqtSignal(bool, str)

    def __init__(self):
        super().__init__()
        self.__initUi()
        self.__initVal()

    def __initVal(self):
        self.__settings_struct = QSettings('settings.ini', QSettings.IniFormat)
        self.__is_valid = False
        self.__api_key = None
        if not self.__settings_struct.contains('API_KEY'):
            self.__settings_struct.setValue('API_KEY', '')
            self.aiEnabled.emit(False, '')
        else:
            self.__api_key = self.__settings_struct.value('API_KEY', type=str)
            self.__apiLineEdit.setText(self.__api_key)
            self.__setApi()

    def __initUi(self):
        self.__apiLineEdit = QLineEdit()
        self.__apiLineEdit.setPlaceholderText('Write your API Key...')

        self.__apiCheckPreviewLbl = QLabel()
        self.__apiCheckPreviewLbl.setFont(QFont('Arial', 10))

        apiLbl = QLabel('API')

        self.__apiLineEdit.returnPressed.connect(self.__setApi)
        self.__apiLineEdit.setEchoMode(QLineEdit.Password)

        apiBtn = QPushButton('Use')
        apiBtn.clicked.connect(self.__setApi)

        lay = QHBoxLayout()
        lay.addWidget(apiLbl)
        lay.addWidget(self.__apiLineEdit)
        lay.addWidget(apiBtn)
        lay.addWidget(self.__apiCheckPreviewLbl)
        lay.setContentsMargins(0, 0, 0, 0)

        self.setLayout(lay)

    def __setApi(self):
        try:
            api_key = self.__apiLineEdit.text()
            response = requests.get('https://api.openai.com/v1/models', headers={'Authorization': f'Bearer {api_key}'})
            f = response.status_code == 200
            self.aiEnabled.emit(f, api_key)
            if f:
                self.__settings_struct.setValue('API_KEY', api_key)
                self.__apiCheckPreviewLbl.setStyleSheet("color: {}".format(QColor(0, 200, 0).name()))
                self.__apiCheckPreviewLbl.setText('API key is valid')
                self.__is_valid = True
            else:
                raise Exception
        except Exception:
            self.__apiCheckPreviewLbl.setStyleSheet("color: {}".format(QColor(255, 0, 0).name()))
            self.__apiCheckPreviewLbl.setText('API key is invalid')
            self.aiEnabled.emit(False, '')
            self.__is_valid = False

    def isAiEnabled(self):
        return self.__is_valid

    def getApiKey(self):
        return self.__api_key