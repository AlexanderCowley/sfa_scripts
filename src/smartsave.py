from pymel.core.system import Path
from PySide2 import QtWidgets, QtCore
from shiboken2 import wrapInstance
import maya.OpenMayaUI as openMUI
import maya.cmds as cmds
import pymel.core as pmc
import logging

log = logging.getLogger(__name__)


def maya_main_window():
    main_window = openMUI.MQtUtil_mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QDialog)


class SmartSaveUI(QtWidgets.QDialog):
    def __init__(self):
        super(SmartSaveUI, self).__init__(parent=maya_main_window())
        self.setWindowTitle("Smart Save")
        self.setMinimumWidth(500)
        self.setMaximumHeight(200)
        self.setWindowFlags(self.windowFlags() ^
                            QtCore.Qt.WindowContextHelpButtonHint)
        self.scenefile = SceneFile()
        self.create_ui()
        self.create_connections()

    def create_ui(self):
        self.title_label = QtWidgets.QLabel("Smart Save")
        self.title_label.setStyleSheet("font: bold 20px")
        self.folder_lay = self._create_folder_ui()
        self.descriptor_header_label = QtWidgets.QLabel("Descriptor")
        self.filename_lay = self._create_filename_ui()
        self.btn_layout = self._create_button_ui()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.folder_lay)
        self.main_layout.addLayout(self.filename_lay)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.btn_layout)
        self.setLayout(self.main_layout)

    def _create_button_ui(self):
        self.save_btn = QtWidgets.QPushButton("Save")
        self.save_increment_btn = QtWidgets.QPushButton(
            "Save Increment")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.save_btn)
        layout.addWidget(self.save_increment_btn)
        layout.addWidget(self.cancel_btn)
        return layout

    def _create_filename_ui(self):
        layout = self._create_filename_headers()
        self.descriptor_le = QtWidgets.QLineEdit(
            self.scenefile.descriptor)
        self.descriptor_le.setMinimumWidth(100)
        self.task_le = QtWidgets.QLineEdit(self.scenefile.task)
        self.task_le.setFixedWidth(56)
        self.ver_sbx = QtWidgets.QSpinBox()
        self.ver_sbx.setButtonSymbols(
            QtWidgets.QAbstractSpinBox.PlusMinus)
        self.ver_sbx.setFixedWidth(50)
        self.ver_sbx.setValue(self.scenefile.ver)
        self.ext_label = QtWidgets.QLabel(".ma")
        layout.addWidget(self.descriptor_le, 1, 0)
        layout.addWidget(QtWidgets.QLabel("_"), 1, 1)
        layout.addWidget(self.task_le, 1, 2)
        layout.addWidget(QtWidgets.QLabel("_v"), 1, 3)
        layout.addWidget(self.ver_sbx, 1, 4)
        layout.addWidget(self.ext_label, 1, 5)
        return layout

    def _create_filename_headers(self):
        self.descriptor_header_label.setStyleSheet("font: bold")
        self.task_header_label = QtWidgets.QLabel("Task")
        self.task_header_label.setStyleSheet("font: bold")
        self.ver_header_label = QtWidgets.QLabel("Version")
        self.ver_header_label.setStyleSheet("font: bold")
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.descriptor_header_label, 0, 0)
        layout.addWidget(self.task_header_label, 0, 2)
        layout.addWidget(self.ver_header_label, 0, 4)
        return layout

    def _create_folder_ui(self):
        default_folder = Path(cmds.workspace
                              (rootDirectory=True, query=True))
        default_folder = default_folder / "scenes"
        self.folder_le = QtWidgets.QLineEdit(default_folder)
        self.folder_browse_button = QtWidgets.QPushButton("...")
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.folder_le)
        layout.addWidget(self.folder_browse_button)
        return layout

    def create_connections(self):
        self.save_btn.clicked.connect(self._save)
        self.save_increment_btn.clicked.connect(self._save_increment())
        self.cancel_btn.clicked.connect(self._cancel)
        self.folder_browse_button.clicked.connect(self._browse_dir)

    @QtCore.Slot()
    def _cancel(self):
        self.close()

    @QtCore.Slot()
    def _save_increment(self):
        self._set_scenefile_properties_from_ui()
        self.scenefile.save_increment()
        self.ver_sbx.setValue(self.scenefile.ver)

    @QtCore.Slot()
    def _save(self):
        self._set_scenefile_properties_from_ui()
        self.scenefile.save()

    def _set_scenefile_properties_from_ui(self):
        self.scenefile.folder_path = self.folder_le.text()
        self.scenefile.descriptor = self.descriptor_le.text()
        self.scenefile.task = self.task_le.text()
        self.scenefile.ver = self.ver_sbx.value()
        self.scenefile.ext = self.ext_label.text()

    @QtCore.Slot()
    def _browse_dir(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Directory", self.folder_le.text(),
            QtWidgets.QFileDialog.ShowDirsOnly |
            QtWidgets.QFileDialog.DontResolveSymlinks)
        self.folder_le.setText(directory)


class SceneFile(object):
    """An abstract representation of a Scene File"""

    def __init__(self, path=None):
        self._folder_path = Path(cmds.workspace(query=True,
                                                rootDirectory=True)
                                 ) / "scenes"
        self.descriptor = "main"
        self.task = "model"
        self.ver = 1
        self.ext = ".ma"
        scene = pmc.system.sceneName()
        if not path and scene:
            path = scene
        if not path and not scene:
            log.warning("Initialize with default properties")
            return
        self._init_from_path(path)

    @property
    def folder_path(self):
        return self._folder_path

    @folder_path.setter
    def folder_path(self, new_val):
        self._folder_path = Path(new_val)

    @property
    def filename(self):
        pattern = "{descriptor}_{task}_v{ver:03d}{ext}"
        return pattern.format(descriptor=self.descriptor,
                              task=self.task, ver=self.ver,
                              ext=self.ext)

    @property
    def path(self):
        return self.folder_path / self.filename

    def _init_from_path(self, path):
        path = Path(path)
        self.folder_path = path.parent
        self.ext = path.ext
        self.descriptor, self.task, ver = path.name. \
            stripext().split("_")
        self.ver = int(ver.split("v")[-1])

    def save(self):
        try:
            return pmc.system.saveAs(self.path)
        except RuntimeError as err:
            log.warning("Missing directory in path. "
                        "Creating directories...")
            self.folder_path.makedirs_p()
            return pmc.system.saveAs(self.path)

    def next_avail_version(self):
        pattern = "{descriptor}_{task}_v*{ext}".format(
            descriptor=self.descriptor, task=self.task, ver=self.ver,
            ext=self.ext)
        matching_scenefiles = []
        for file_ in self.folder_path.files():
            if file_.name.fnmatch(pattern):
                matching_scenefiles.append(file_)
        if not matching_scenefiles:
            return 1
        matching_scenefiles.sort(reverse=True)
        latest_scene_files = matching_scenefiles[0]
        latest_scene_files = latest_scene_files.name.stripext()
        latest_scene_num = int(latest_scene_files.split("_v")[-1])
        return latest_scene_num + 1

    def save_increment(self):
        self.ver = self.next_avail_version()
        self.save()
