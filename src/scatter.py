from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as openMUI
import maya.cmds as cmds
import logging
import random

random.seed(1465)

log = logging.getLogger(__name__)


class ScatterUI(QtWidgets.QDialog):

    def __init__(self):
        pass


"Needs:"
"When applied:"
"Randomize the Scale: Have the user determine the min and max of scale"
"Must be for all three axis"
"Have it start at 1.0 and increase based on that. 1.20 is 20% scaled"
"Must be applied to the transform node attributes of the instance"
"Randomize Rotation Offset: User specifies min max"
"Angle must be specified in degrees from 0 to 360"
"Must be applied to the transform node attributes"


class ScatterData(object):

    def __init__(self, source_object=None, destination_object=None):
        self.source_object = source_object
        self.destination_object = destination_object
        self.vert_list = self.get_vertices(destination_object)
        self.create_instances(source_object, self.vert_list)
        if not source_object:
            log.warning("Select a source object to scatter")
        if not destination_object:
            log.warning("Select a destination to scatter to")

    def get_vertices(self, destination_obj):
        self.obj_instances = cmds.ls(destination_obj,
                                     orderedSelection=True,
                                     flatten=True)
        self.obj_instances = \
            cmds.polyListComponentConversion(self.obj_instances,
                                             toVertex=True)
        self.obj_instances = \
            cmds.filterExpand(self.obj_instances, selectionMask=31,
                              expand=True)
        return self.obj_instances

    def create_instances(self, source, num_vertices):
        self.grp_instances = cmds.group(empty=True,
                                        name="grp_scatter#")
        for self.instance in num_vertices:
            self.source_instance = \
                cmds.instance(source,
                              name=source + "inst_#")
            cmds.parent(self.source_instance,
                        self.grp_instances)
            self.move_instances(self.instance, self.source_instance)
            self.random_rot(self.source_instance)
            self.random_scaling(self.source_instance)

    def move_instances(self, inst_vert, inst_source):
        self.pos = cmds.xform([inst_vert], query=True, translation=True,
                              worldSpace=True)
        cmds.xform(inst_source, translation=self.pos)

    def random_rot(self, result):
        random_rot = random.uniform(0, 360)
        cmds.rotate(random_rot, random_rot, random_rot, result)

    def random_scaling(self, result):
        min_val = 1
        max_val = 5
        random_scale = random.uniform(min_val, max_val)
        cmds.scale(random_scale, random_scale,
                   random_scale, result)

