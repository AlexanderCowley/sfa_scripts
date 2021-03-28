import sys
from PySide2 import QtWidgets


class ComboBox(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ComboBox, self).__init__(parent)
        self.setWindowTitle("Combo Box Example")
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_layout(self):
        self.lay = QtWidgets.QVBoxLayout()
        self.lay.addWidget(self.ext_lbl)
        self.lay.addLayout(self.ext_cmb)
        self.setLayout(self.lay)

    def create_widgets(self):
        self.ext_lbl = QtWidgets.QLabel()
        self.ext_cmb = QtWidgets.QComboBox()
        "add item and add items are used for example purposes only"
        "No reason that .hip is separated"
        self.ext_cmb.addItem(".hip")
        self.ext_cmb.addItems(['.ma', '.mb'])

    def create_connections(self):
        self.ext_cmb.currentIndexChanged(self._update_ext_lbl())

    def _update_ext_lbl(self):
        self.ext_lbl.setText(self.ext_cmb.currentText())
