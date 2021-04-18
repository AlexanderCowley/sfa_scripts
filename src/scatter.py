from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as openMUI
import maya.cmds as cmds
import logging
import random

random.seed(1465)

log = logging.getLogger(__name__)


def maya_main_window():
    main_window = openMUI.MQtUtil_mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QDialog)


class ScatterUI(QtWidgets.QDialog):

    def __init__(self):
        super(ScatterUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Scatter Tool")
        self.setMinimumWidth(500)
        self.setMaximumWidth(700)
        self.setMinimumHeight(500)
        self.setMaximumHeight(700)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.scatter_data = ScatterData()
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.title_label = QtWidgets.QLabel("Scatter")
        self.title_label.setStyleSheet("font: bold 20px")
        self.source_header_lbl = QtWidgets.QLabel("Source Object")
        self.destination_header_lbl = \
            QtWidgets.QLabel("Destination Object")
        self.object_layout = self._select_objects_layout()
        self.button_layout = self._create_buttons_ui()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.object_layout)
        self.main_layout.addLayout(self.button_layout)
        self.setLayout(self.main_layout)

    def _select_objects_layout(self):
        layout = self._create_object_headers()
        self.source_obj_cmbo = QtWidgets.QComboBox()
        self.dest_obj_cmbo = QtWidgets.QComboBox()
        self.source_obj_cmbo_init = self._create_combo_list()
        self.dest_obj_cmbo_init = self._create_combo_list()
        self.source_obj_cmbo.setMinimumWidth(130)
        self.source_obj_cmbo.setMaximumWidth(150)
        self.source_obj_cmbo.addItems(self.source_obj_cmbo_init)
        self.dest_obj_cmbo.setMinimumWidth(130)
        self.dest_obj_cmbo.setMaximumWidth(150)
        self.dest_obj_cmbo.addItems(self.dest_obj_cmbo_init)
        layout.addWidget(self.source_obj_cmbo, 3, 1)
        layout.addWidget(self.dest_obj_cmbo, 2, 1)
        return layout

    def _create_combo_list(self):
        self.outline_list = cmds.ls(geometry=True)
        return self.outline_list

    def _create_object_headers(self):
        self.source_header_lbl = QtWidgets.QLabel("Source Object")
        self.source_header_lbl.setStyleSheet("font: bold 20px")
        self.destination_header_lbl = \
            QtWidgets.QLabel("Destination Object")
        self.destination_header_lbl.setStyleSheet("font: bold 20px")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.source_header_lbl, 3, 0)
        layout.addWidget(self.destination_header_lbl, 2, 0)
        return layout

    def _create_buttons_ui(self):
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_btn)
        layout.addWidget(self.cancel_btn)
        return layout

    def create_connections(self):
        self.scatter_btn.clicked.connect(self._scatter)
        self.cancel_btn.clicked.connect(self._cancel)

    @QtCore.Slot()
    def _scatter(self):
        self._set_object_properties_ui()
        self.scatter_data.get_vertices()

    @QtCore.Slot()
    def _cancel(self):
        self.close()

    def _set_object_properties_ui(self):
        self.scatter_data.source = self.source_obj_cmbo.currentText()
        self.scatter_data.destination = self.dest_obj_cmbo.currentText()


class ScatterData(object):

    def __init__(self, source_object=None, destination_object=None):
        self._source = ""
        self._destination = ""
        self._min_rot_range = 1
        self._max_rot_range = 1
        self._min_scale_range = 1
        self._max_scale_range = 1
        if not source_object:
            log.warning("Select a source object to scatter")
            return
        if not destination_object:
            log.warning("Select a destination to scatter to")
            return
        self._init_from_objects()

    @property
    def source(self):
        return self._source

    @source.setter
    def source(self, new_value):
        self._source = new_value

    @property
    def destination(self):
        return self._destination

    @destination.setter
    def destination(self, new_value):
        self._destination = new_value

    @property
    def min_rot_range(self):
        return self._min_rot_range

    @min_rot_range.setter
    def min_rot_range(self, new_value):
        self.min_rot_range = new_value

    @property
    def max_rot_range(self):
        return self._max_rot_range

    @max_rot_range.setter
    def max_rot_range(self, new_value):
        self._max_rot_range = new_value

    @property
    def min_scale_range(self):
        return self._min_scale_range

    @min_scale_range.setter
    def min_scale_range(self, new_value):
        self._min_scale_range = new_value

    @property
    def max_scale_range(self):
        return self._max_scale_range

    @max_scale_range.setter
    def max_scale_range(self, new_value):
        self._max_scale_range = new_value

    def get_vertices(self):
        self.obj_instances = \
            cmds.polyListComponentConversion(self.destination,
                                             toVertex=True)
        self.obj_instances = cmds.ls(self.obj_instances, flatten=True)
        self.obj_instances = \
            cmds.filterExpand(self.obj_instances, selectionMask=31,
                              expand=True)
        self.create_instances(self.obj_instances)

    def create_instances(self, num_vertices):
        self.grp_instances = cmds.group(empty=True,
                                        name="group_scatter#")
        for instance in num_vertices:
            self.source_instance = \
                cmds.instance(self.source,
                              name=self.source + "inst_#")
            cmds.parent(self.source_instance,
                        self.grp_instances)
            self.move_instances(instance, self.source_instance)
            self.random_rot(self.source_instance)
            self.random_scaling(self.source_instance)

    def move_instances(self, inst_vert, inst_source):
        self.pos = cmds.xform(inst_vert, query=True, translation=True,
                              worldSpace=True)
        cmds.xform(inst_source, translation=self.pos)

    def random_rot(self, result):
        print("Rotation Result: " + str(result))
        self.random_seed = random.uniform(0, 360)
        cmds.rotate(self.random_seed, self.random_seed,
                    self.random_seed, result)

    def random_scaling(self, result):
        self.min_val = 1
        self.max_val = 5
        random_scale = random.uniform(self.min_val, self.max_val)
        cmds.scale(random_scale, random_scale, random_scale, result)

    def _init_from_objects(self, source_object, destination_object):
        self._source = source_object
        self._destination = destination_object

