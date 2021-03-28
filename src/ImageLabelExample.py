import sys
from PySide2 import QtWidgets, QtGui, QtCore


class ImageLabelExample(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ImageLabelExample, self).__init__(parent)
        self.setWindowTitle("Image Label Example")
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        self.image_lbl = QtWidgets.QLabel()
        self.image_lbl.setPixmap(QtGui.QPixmap("starship.png"))
        self.image_btn = QtWidgets.QPushButton()
        self.image_btn.setIcon(QtGui.QIcon("starship.png"))
        self.image_btn.setIconSize(QtCore.QSize(32, 32))

    def create_layout(self):
        self.lay = QtWidgets.QVBoxLayout()
        self.lay.addWidget(self.image_lbl)
        self.lay.addWidget(self.image_btn)
        self.setLayout(self.lay)
