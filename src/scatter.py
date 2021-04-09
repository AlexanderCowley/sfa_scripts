from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as openMUI
import maya.cmds as cmds


class ScatterUI(QtWidgets.QDialog):

    def __init__(self):
        pass


"Needs:"
"A SOURCE OBJECT to scatter"
"A DESTINATION: Can either be an object or vertices"
"When applied:"
"INSTANCES must be created of the source object. NOT copies."
"MOVE the source object onto the DESTINATION VERTICES of the " \
    "selected object"
"Randomize the Scale: Have the user determine the min and max of scale"
"Must be for all three axis"
"Have it start at 1.0 and increase based on that. 1.20 is 20% scaled"
"Must be applied to the transform node attributes of the instance"
"Randomize Rotation Offset: User specifies min max"
"Angle must be specified in degrees from 0 to 360"
"Must be applied to the transform node attributes"


class ScatterData(object):

    def __init__(self):
        pass
