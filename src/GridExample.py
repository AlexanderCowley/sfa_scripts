import sys
from PySide2 import QtWidgets


class GridLayout(QtWidgets.QDialog):

    def __init__(self, parent = None):
        super(GridLayout, self).__init__(parent)
        self.setWindowTitle("Grid Layout Example")
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.btn1 = QtWidgets.QPushButton("Hello1")
        self.btn2 = QtWidgets.QPushButton("Hello2")
        self.btn3 = QtWidgets.QPushButton("Hello3")
        self.btn4 = QtWidgets.QPushButton("Hello4")

    def create_layout(self):
        self.gridlayout = QtWidgets.QGridLayout()
        self.gridlayout.addWidget(self.btn1, 0, 0)
        self.gridlayout.addWidget(self.btn2, 0, 1)
        self.gridlayout.addWidget(self.btn1, 1, 0)
        self.gridlayout.addWidget(self.btn1, 1, 1)
        self.setLayout(self.gridlayout)
