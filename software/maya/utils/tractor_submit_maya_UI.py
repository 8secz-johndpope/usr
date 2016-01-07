'''
In maya run this at the moment....

import sys
sys.path.append("/Users/Shared/UTS_Dev/gitRepositories/utsdab/usr")

from software.maya.utils import tractor_submit_maya_UI
reload(tractor_submit_maya_UI)
tractor_submit_maya_UI.create()

'''


import PySide.QtCore as qc
import PySide.QtGui as qg
import sys
import os
from software.renderfarm.dabtractor.factories import user_factory as ufac
from software.renderfarm.dabtractor.factories import interface_factory as ifac

from functools import partial

try:
    import maya.cmds  as mc
    import pymel.core as pm
    # from utils.generic import undo
    # import sip
    import shiboken
    import maya.OpenMayaUI as mui
except Exception,err:
    print "No maya import {}".format(err)


# -------------------------------------------------------------------------------------------------------------------- #

class TractorSubmit(qg.QDialog):
    def __init__(self):
        super(TractorSubmit,self).__init__()
        self.setWindowTitle('UTS_FARM_SUBMIT')
        self.setObjectName('UTS_FARM_SUBMIT')
        self.setWindowFlags(qc.Qt.WindowStaysOnTopHint)
        main_widget = TractorSubmitWidget()
        self.setLayout(qg.QVBoxLayout())
        self.setFixedWidth(314)

        scroll_area=qg.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFocusPolicy(qc.Qt.NoFocus)
        self.layout().addWidget(scroll_area)


        self.layout().setContentsMargins(3,3,3,3)
        self.layout().addWidget(main_widget)
        scroll_area.setWidget(main_widget)

        self._dock_widget = self._dock_name = None

    #------------------------------------------------------------------------------------------#

    def connectDockWidget(self, dock_name, dock_widget):
        self._dock_widget = dock_widget
        self._dock_name   = dock_name


    def close(self):
        if self._dock_widget:
            mc.deleteUI(self._dock_name)
        else:
            qg.QDialog.close(self)
        self._dock_widget = self._dock_name = None


# -------------------------------------------------------------------------------------------------------------------- #
class TractorSubmitWidget(qg.QFrame):
    def __init__(self):
        super(TractorSubmitWidget, self).__init__()

        self.setFrameStyle(qg.QFrame.Panel | qg.QFrame.Raised)
        self.setSizePolicy(qg.QSizePolicy.Minimum,
                           qg.QSizePolicy.Fixed)

        self.setLayout(qg.QVBoxLayout())

        self.layout().setContentsMargins(3,3,3,3)
        self.layout().setSpacing(0)
        self.layout().setAlignment(qc.Qt.AlignTop)

        # ------------------------------------------------------------------------------------ #
        # USER WIDGET
        user_widget = ifac.UserWidget()
        self.layout().addWidget(user_widget)

        self.stacked_layout = qg.QStackedLayout()
        self.layout().addLayout(self.stacked_layout)

        self.mode_splitter = ifac.Splitter("MODE")
        self.layout().addWidget(self.mode_splitter)

        grid_widget = qg.QWidget()
        grid_widget.setLayout(qg.QGridLayout())
        grid_widget.layout().setContentsMargins(3,3,3,3)

        # button_layout.setLayout(qg.QGridLayout())
        # button_layout = qg.QGridLayout()
        layout_1_bttn = qg.QPushButton('Maya')
        layout_2_bttn = qg.QPushButton('Mental Ray')
        layout_3_bttn = qg.QPushButton('Renderman')
        layout_4_bttn = qg.QPushButton('Bash Cmd')
        layout_5_bttn = qg.QPushButton('Nuke')
        layout_6_bttn = qg.QPushButton('Archive')

        grid_widget.layout().addWidget(layout_1_bttn,0,0)
        grid_widget.layout().addWidget(layout_2_bttn,0,1)
        grid_widget.layout().addWidget(layout_3_bttn,0,2)
        grid_widget.layout().addWidget(layout_4_bttn,1,0)
        grid_widget.layout().addWidget(layout_5_bttn,1,1)
        grid_widget.layout().addWidget(layout_6_bttn,1,2)

        self.layout().addWidget(grid_widget)

        # ------------------------------------------------------------------------------------ #
        # SCENE WIDGET
        scene_widget = ifac.SceneWidget()
        # self.layout().addWidget(scene_widget)

        # RANGE WIDGET
        range_widget = ifac.RangeWidget()
        # self.layout().addWidget(range_widget)

        # MAYA WIDGET
        maya_widget= ifac.MayaWidget()
        # self.layout().addWidget(maya_widget)

        # MENTALRAY WIDGET
        mentalray_widget= ifac.MentalRayWidget()
        # self.layout().addWidget(maya_widget)

        # RENDERMAN WIDGET
        renderman_widget= ifac.RendermanWidget()
        # self.layout().addWidget(renderman_widget)

        # BASH WIDGET
        bash_widget= ifac.BashWidget()
        # self.layout().addWidget(bash_widget)

        # ARCHIVE WIDGET
        archive_widget= ifac.ArchiveWidget()
        # self.layout().addWidget(bash_widget)

        # NUKE WIDGET
        nuke_widget= ifac.NukeWidget()
        # self.layout().addWidget(bash_widget)

        # TRACTOR WIDGET
        tractor_widget= ifac.TractorWidget()
        # self.layout().addWidget(tractor_widget)

        # FARM JOB EXTRAS WIDGET
        # farm_extras_widget = qg.QWidget()
        # farm_extras_widget.setLayout(qg.QVBoxLayout())
        # farm_extras_widget.layout().setSpacing(2)
        # farm_extras_widget.layout().setContentsMargins(0,0,0,0)

        # TEST WIDGET
        # test_widget = Test()

        # ------------------------------------------------------------------------------------ #

        self.path="/Users/Shared/UTS_Dev/dabrender"

        self.stacked_layout.addWidget(maya_widget)
        self.stacked_layout.addWidget(mentalray_widget)
        self.stacked_layout.addWidget(renderman_widget)
        self.stacked_layout.addWidget(bash_widget)
        self.stacked_layout.addWidget(nuke_widget)
        self.stacked_layout.addWidget(archive_widget)

        layout_1_bttn.clicked.connect(partial(self.stacked_layout.setCurrentIndex, 0))
        layout_2_bttn.clicked.connect(partial(self.stacked_layout.setCurrentIndex, 1))
        layout_3_bttn.clicked.connect(partial(self.stacked_layout.setCurrentIndex, 2))
        layout_4_bttn.clicked.connect(partial(self.stacked_layout.setCurrentIndex, 3))
        layout_5_bttn.clicked.connect(partial(self.stacked_layout.setCurrentIndex, 4))
        layout_6_bttn.clicked.connect(partial(self.stacked_layout.setCurrentIndex, 5))


# -------------------------------------------------------------------------------------------------------------------- #
dialog = None

def create(docked=True):
    global dialog

    if dialog is None:
        dialog = TractorSubmit()

    if docked is True:
        ptr = mui.MQtUtil.mainWindow()
        main_window = shiboken.wrapInstance(long(ptr), qg.QWidget)

        dialog.setParent(main_window)
        size = dialog.size()

        name = mui.MQtUtil.fullName(long(shiboken.getCppPointer(dialog)[0]))
        dock = mc.dockControl(
            allowedArea =['right', 'left'],
            area        = 'right',
            floating    = False,
            content     = name,
            width       = size.width(),
            height      = size.height(),
            label       = 'UTS_FARM_SUBMIT')

        widget      = mui.MQtUtil.findControl(dock)
        dock_widget = shiboken.wrapInstance(long(widget), qg.QWidget)
        dialog.connectDockWidget(dock, dock_widget)

    else:
        dialog.show()


def delete():
    global dialog
    if dialog:
        dialog.close()
        dialog = None

def getMayaWindow():
    """
    Get the main Maya window as a QtGui.QMainWindow instance
    @return: QtGui.QMainWindow instance of the top level Maya windows
    """
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return shiboken.wrapInstance(long(ptr), qg.QWidget)
# -------------------------------------------------------------------------------------------------------------------- #

def main():

    app = qg.QApplication(sys.argv)
    dialog = TractorSubmit()
    dialog.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()