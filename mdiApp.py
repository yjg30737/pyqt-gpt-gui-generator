from PyQt5.QtWidgets import QMdiArea
from PyQt5.QtWidgets import QMdiSubWindow


class MdiArea(QMdiArea):
    def __init__(self):
        super().__init__()

    def clearSubWindow(self):
        for sub in self.subWindowList():
            sub.close()

    def createSubWindow(self, window):
        # Only one subwindow at a time
        # Create a new subwindow
        print(window)
        subWindow = QMdiSubWindow()
        subWindow.setWidget(window)
        self.addSubWindow(subWindow)
        subWindow.showMaximized()
