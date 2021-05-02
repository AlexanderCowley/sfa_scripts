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
        self.object_layout = self._select_objects_layout()
        self.button_layout = self._create_buttons_layout()
        self.spinbox_layout = self._create_spinbox_layout()
        self.source_header_lbl = QtWidgets.QLabel("Source Object")
        self.destination_header_lbl = \
            QtWidgets.QLabel("Destination Object")
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.object_layout)
        #Align Checkbox
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.spinbox_layout)
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
        layout.addWidget(self.source_obj_cmbo, 0, 0)
        layout.addWidget(self.dest_obj_cmbo, 2, 0)
        return layout

    def _create_combo_list(self):
        self.outline_list = cmds.ls(geometry=True)
        return self.outline_list

    def _create_object_headers(self):
        self.source_header_lbl = QtWidgets.QLabel("Source")
        self.source_header_lbl.setStyleSheet("font: bold 20px")
        self.destination_header_lbl = \
            QtWidgets.QLabel("Destination")
        self.destination_header_lbl.setStyleSheet("font: bold 20px")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.source_header_lbl, 0, 2)
        layout.addWidget(self.destination_header_lbl, 2, 2)
        return layout

    def _create_buttons_layout(self):
        self.scatter_btn = QtWidgets.QPushButton("Scatter")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.scatter_btn)
        layout.addWidget(self.cancel_btn)
        return layout

    def _create_spinbox_layout(self):
        self.sbx_collection = self._create_sbx_list()
        self.sbx_collection = \
            self._set_sbx_attributes(self.sbx_collection)
        self.sbx_collection = self._set_sbx_values(self.sbx_collection)
        layout = self._create_spinbox_headers()
        layout.addWidget(self.sbx_collection[0], 2, 2)
        layout.addWidget(self.sbx_collection[1], 2, 3)
        layout.addWidget(self.sbx_collection[2], 3, 2)
        layout.addWidget(self.sbx_collection[3], 3, 3)
        layout.addWidget(self.sbx_collection[4], 4, 2)
        layout.addWidget(self.sbx_collection[5], 4, 3)

        layout.addWidget(self.sbx_collection[6], 2, 6)
        layout.addWidget(self.sbx_collection[7], 2, 7)
        layout.addWidget(self.sbx_collection[8], 3, 6)
        layout.addWidget(self.sbx_collection[9], 3, 7)
        layout.addWidget(self.sbx_collection[10], 4, 6)
        layout.addWidget(self.sbx_collection[11], 4, 7)
        return layout

    def _create_spinbox_headers(self):
        self.rotation_header = QtWidgets.QLabel("Rotate")
        self.rotation_header.setStyleSheet("font: bold 20px")
        self.min_rot_header = QtWidgets.QLabel("Min")
        self.max_rot_header = QtWidgets.QLabel("Max")
        self.scale_header = QtWidgets.QLabel("Scale")
        self.scale_header.setStyleSheet("font: bold 20px")
        self.min_scale_header = QtWidgets.QLabel("Min")
        self.max_scale_header = QtWidgets.QLabel("Max")
        self._x_lbl_rot = QtWidgets.QLabel("X")
        self._y_lbl_rot = QtWidgets.QLabel("Y")
        self._z_lbl_rot = QtWidgets.QLabel("Z")
        self._x_lbl_scale = QtWidgets.QLabel("X")
        self._y_lbl_scale = QtWidgets.QLabel("Y")
        self._z_lbl_scale = QtWidgets.QLabel("Z")
        layout = QtWidgets.QGridLayout()
        layout.setColumnStretch(0, 1)
        layout.addWidget(self.rotation_header, 0, 2)
        layout.addWidget(self.scale_header, 0, 6)
        layout.addWidget(self.min_rot_header, 1, 3)
        layout.addWidget(self.max_rot_header, 1, 2)
        layout.addWidget(self.min_scale_header, 1, 6)
        layout.addWidget(self.max_scale_header, 1, 7)
        layout.addWidget(self._x_lbl_rot, 2, 1)
        layout.addWidget(self._y_lbl_rot, 3, 1)
        layout.addWidget(self._z_lbl_rot, 4, 1)
        layout.addWidget(self._x_lbl_scale, 2, 5)
        layout.addWidget(self._y_lbl_scale, 3, 5)
        layout.addWidget(self._z_lbl_scale, 4, 5)
        return layout

    def _create_sbx_list(self):
        spin_boxes = []
        self.min_rot_x_sbx = QtWidgets.QSpinBox()
        spin_boxes.append(self.min_rot_x_sbx)
        self.max_rot_x_sbx = QtWidgets.QSpinBox()
        spin_boxes.append(self.max_rot_x_sbx)
        self.min_rot_y_sbx = QtWidgets.QSpinBox()
        spin_boxes.append(self.min_rot_y_sbx)
        self.max_rot_y_sbx = QtWidgets.QSpinBox()
        spin_boxes.append(self.max_rot_y_sbx)
        self.min_rot_z_sbx = QtWidgets.QSpinBox()
        spin_boxes.append(self.min_rot_z_sbx)
        self.max_rot_z_sbx = QtWidgets.QSpinBox()
        spin_boxes.append(self.max_rot_z_sbx)

        self.min_scale_x_sbx = QtWidgets.QSpinBox()
        spin_boxes.append(self.min_scale_x_sbx)
        self.max_scale_x_sbx = QtWidgets.QSpinBox()
        spin_boxes.append(self.max_scale_x_sbx)
        self.min_scale_y_sbx = QtWidgets.QSpinBox()
        spin_boxes.append(self.min_scale_y_sbx)
        self.max_scale_y_sbx = QtWidgets.QSpinBox()
        spin_boxes.append(self.max_scale_y_sbx)
        self.min_scale_z_sbx = QtWidgets.QSpinBox()
        spin_boxes.append(self.min_scale_z_sbx)
        self.max_scale_z_sbx = QtWidgets.QSpinBox()
        spin_boxes.append(self.max_scale_z_sbx)
        return spin_boxes

    def _set_sbx_attributes(self, sbx_list):
        for sbx in sbx_list:
            sbx.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
            sbx.setFixedWidth(80)
            sbx.setRange(000, 360)
        return sbx_list

    def _set_sbx_values(self, sbx):
        self._set_sbx_rot_values(sbx)
        self._set_sbx_scale_values(sbx)
        return sbx

    def _set_sbx_rot_values(self, sbx):
        sbx[0].setValue(self.scatter_data.min_rot_range[0])
        sbx[1].setValue(self.scatter_data.max_rot_range[0])
        sbx[2].setValue(self.scatter_data.min_rot_range[1])
        sbx[3].setValue(self.scatter_data.max_rot_range[1])
        sbx[4].setValue(self.scatter_data.min_rot_range[2])
        sbx[5].setValue(self.scatter_data.max_rot_range[2])

    def _set_sbx_scale_values(self, sbx):
        sbx[6].setValue(self.scatter_data.min_scale_range[0])
        sbx[7].setValue(self.scatter_data.max_scale_range[0])
        sbx[8].setValue(self.scatter_data.min_scale_range[1])
        sbx[9].setValue(self.scatter_data.max_scale_range[1])
        sbx[10].setValue(self.scatter_data.min_scale_range[2])
        sbx[11].setValue(self.scatter_data.max_scale_range[2])

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
        self._set_destination_obj()
        self.scatter_data.source = self.source_obj_cmbo.currentText()
        self._set_rot_sbx_properties_ui()
        self._set_scale_sbx_properties_ui()

    def _set_scale_sbx_properties_ui(self):
        self.scatter_data.min_scale_range[0] = \
            self.min_scale_x_sbx.value()
        self.scatter_data.max_scale_range[0] = \
            self.max_scale_x_sbx.value()
        self.scatter_data.min_scale_range[1] = \
            self.min_scale_y_sbx.value()
        self.scatter_data.max_scale_range[1] = \
            self.max_scale_y_sbx.value()
        self.scatter_data.min_scale_range[2] = \
            self.min_scale_z_sbx.value()
        self.scatter_data.max_scale_range[2] = \
            self.max_scale_z_sbx.value()

    def _set_rot_sbx_properties_ui(self):
        self.scatter_data.min_rot_range[0] = self.min_rot_x_sbx.value()
        self.scatter_data.max_rot_range[0] = self.max_rot_x_sbx.value()
        self.scatter_data.min_rot_range[1] = self.min_rot_y_sbx.value()
        self.scatter_data.max_rot_range[1] = self.max_rot_y_sbx.value()
        self.scatter_data.min_rot_range[2] = self.min_rot_z_sbx.value()
        self.scatter_data.max_rot_range[2] = self.max_rot_z_sbx.value()

    def _set_destination_obj(self):
        if len(cmds.ls(selection=True)) != 0:
            self.scatter_data.destination = \
                self.scatter_data.selection_to_vertices(
                    cmds.ls(selection=True))
        else:
            self.scatter_data.destination = \
                self.dest_obj_cmbo.currentText()


class ScatterData(object):

    def __init__(self, source_object=None, destination_object=None):
        self._source = ""
        self._destination = ""
        self.min_rot_range = [0, 0, 0]
        self.max_rot_range = [360, 360, 360]
        self.min_scale_range = [1, 1, 1]
        self.max_scale_range = [2, 2, 2]
        self.selection_percentage = 100
        cmds.select(clear=True)
        if not source_object and not destination_object:
            self._init_from_objects(source_object, destination_object)
        if not source_object:
            log.warning("Select a source object to scatter")
            return
        if not destination_object:
            log.warning("Select a destination to scatter to")
            return

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
        self.random_seed = \
            [random.uniform(self.min_rot_range[0],
                            self.max_rot_range[0]),
             random.uniform(self.min_rot_range[1],
                            self.max_rot_range[1]),
             random.uniform(self.min_rot_range[2],
                            self.max_rot_range[2])]
        cmds.rotate(self.random_seed[0], self.random_seed[1],
                    self.random_seed[2], result)

    def random_scaling(self, result):
        random_scale = \
            [random.uniform(self.min_scale_range[0],
                            self.max_scale_range[0]),
             random.uniform(self.min_scale_range[1],
                            self.max_scale_range[1]),
             random.uniform(self.min_scale_range[2],
                            self.max_scale_range[2])]
        cmds.scale(random_scale[0], random_scale[1], random_scale[2],
                   result)

    def _init_from_objects(self, source_object, destination_object):
        self._source = source_object
        self._destination = destination_object
        self.selection_percentage = 100
        for i in range(len(self.min_scale_range)):
            self.min_scale_range[i] = 1
        for i in range(len(self.max_scale_range)):
            self.max_scale_range[i] = 1
        for i in range(len(self.min_rot_range)):
            self.min_rot_range[i] = 0
        for i in range(len(self.max_rot_range)):
            self.max_rot_range[i] = 0

    def selection_to_vertices(self, vert_source):
        vert_source = cmds.ls(selection=True, flatten=True)
        vert_source = cmds.polyListComponentConversion(vert_source,
                                                       toVertex=True)
        vert_source = cmds.filterExpand(vert_source,
                                        selectionMask=31)
        percent_amount = self.calc_percentage(len(vert_source),
                             self.selection_percentage)
        print("Amount of Vertices per percent: " + str(percent_amount))
        print("Vertices List: " + str(vert_source))
        vert_source = \
            self.randomize_vertices_selection(
                percent_amount, vert_source)
        return vert_source

    def calc_percentage(self, list_len, percentage):
        if not list_len:
            log.warning("Cannot add percentage without a length")
            return
        if list_len <= 0:
            log.warning("Invalid Argument")
        if percentage >= 100:
            percentage = 100
        result = int((percentage/float(100)) * list_len)
        return result

    def randomize_vertices_selection(self, amount, vert_list):
        new_vert_list = random.sample(vert_list, amount)
        return new_vert_list

