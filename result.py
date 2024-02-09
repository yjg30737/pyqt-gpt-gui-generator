import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget

class ListApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        
        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Enter item...")
        self.layout.addWidget(self.input)
        
        self.addButton = QPushButton("Add Item", self)
        self.layout.addWidget(self.addButton)
        self.addButton.clicked.connect(self.addItem)

        self.deleteButton = QPushButton("Delete Selected", self)
        self.layout.addWidget(self.deleteButton)
        self.deleteButton.clicked.connect(self.deleteItem)

        self.listWidget = QListWidget(self)
        self.layout.addWidget(self.listWidget)
        
        self.setLayout(self.layout)
        self.setWindowTitle('List Editor')

    def addItem(self):
        itemText = self.input.text()
        if itemText:  # Ensure non-empty string
            self.listWidget.addItem(itemText)
            self.input.setText("")  # Clear input field after adding

    def deleteItem(self):
        listItems = self.listWidget.selectedItems()
        if not listItems: return        
        for item in listItems:
            self.listWidget.takeItem(self.listWidget.row(item))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ListApp()
    ex.show()
    sys.exit(app.exec_())