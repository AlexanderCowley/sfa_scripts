import maya.OpenMayaUI as omui
from PySide2 import QtWidgets
from shiboken2 import wrapInstance


def maya_main_window():
    main_window = omui.MQtUtil_mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QDialog)

class SimpleUI(QtWidgets.QDialog):

    def __init__(self):
        # Passing SimpleUI arguments to super
        # Makes the class python compatible

        super(SimpleUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("A Simple UI")
