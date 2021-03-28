import sys
from PySide2 import QtWidgets, QtCore


class ListWidget(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ListWidget, self).__init__(parent)
        self.setWindowTitle("List Widget Example")
        self.create_widgets()
        self.create_layout()
        self.create_connections()

    def create_widgets(self):
        self.file_selected_lbl = QtWidgets.QLabel()
        self.files_lw = QtWidgets.QListWidget()
        self._populate_files_list()

    def create_layout(self):
        self.lay = QtWidgets.QVBoxLayout()
        self.lay.addWidget(self.file_selected_lbl)
        self.lay.addWidget(self.files_lw)
        self.setLayout(self.lay)

    def create_connections(self):
        self.files_lw.itemSelectionChanged.connect(
            self._update_file_selected_lbl)

    @QtCore.Slot()
    def _update_file_selected_lbl(self):
        self.file_selected_lbl.setText(
            self.files_lw.currentItem().text())

    def _populate_files_list(self):
        items = ['car.ma', 'monster.ma', 'explosion.hip', 'hero.ma',
                 'castle.ma']
        for item in items:
            lw_item = QtWidgets.QListWidgetItem(item)
            self.files_lw.addItem(lw_item)
