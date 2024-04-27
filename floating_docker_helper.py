import datetime
import json
from os import path
from typing import List

from PyQt5.QtCore import QObject, QTimer, Qt
from PyQt5.QtWidgets import QToolButton, QMenu, QMessageBox, QAction, QWidget, QAbstractScrollArea
from PyQt5.QtGui import QKeySequence, QCursor

from .IntervalTask import *
from .HotReloadExtension import HotReloadExtension
from krita import *
from .util.Logger import Logger
from .utils import active_window, user_input, floating_message, active_view, find_tool_box

EXTENSION_ID = 'pykrita_yuuki_krita_helper'
HELLO_ACTION_ENTRY = 'Say Hello'
INPUT_ECHO_ACTION_ENTRY = 'Echo'

logger = Logger()

fileDir = path.dirname(path.realpath(__file__))

class FloatingDockerHelper(Extension):

    def __init__(self, parent):
        super().__init__(parent)
        self.floating_docker_data = None

    def setup(self):
        pass

    def createActions(self, window):
        trigger_color_selector_on_canvas_mode = window.createAction(EXTENSION_ID + "_trigger_floating_docker",
                                                                    "Trigger floating docker",
                                                                    "tools")
        trigger_color_selector_on_canvas_mode.triggered.connect(lambda: self.trigger_floating_docker())


        trigger_color_selector_on_canvas_mode = window.createAction(EXTENSION_ID + "_save_floating_docker",
                                                                    "Save floating docker Info",
                                                                    "tools")
        # status.triggered.connect(lambda: self.status())
        trigger_color_selector_on_canvas_mode.triggered.connect(lambda: self.save_docker_floating_data())
        self.floating_docker_data = self.load_docker_floating_data()

    def load_docker_floating_data(self):
        try:
            with open(path.join(fileDir, 'datas', 'dockerFloatingData.json'), 'r') as f:
                return json.loads(f.read())
        except BaseException as e:
            return {}


    def save_docker_floating_data(self):
        res = {}
        for docker in Krita.instance().dockers():
            if not docker.isFloating():
                continue
            geo = docker.geometry()
            res[docker.objectName()] = [geo.x(), geo.y(), geo.width(), geo.height()]
            with open(path.join(fileDir, 'datas', 'dockerFloatingData.json'), 'w') as f:
                f.write(json.dumps(res))
        self.floating_docker_data = res
        floating_message("done")

    def trigger_floating_docker(self):
        if self.floating_docker_data is None:
            return

        first_docker_visible = None
        for docker in Krita.instance().dockers():
            if docker.objectName() in self.floating_docker_data:
                docker.setFloating(True)

                if first_docker_visible is None:
                    first_docker_visible = docker.isVisible()

                if first_docker_visible:
                    docker.setVisible(False)
                else:
                    docker.setVisible(True)
                    geo = self.floating_docker_data[docker.objectName()]
                    docker.setGeometry(geo[0], geo[1], geo[2], geo[3])
                    docker.repaint()






        # if not self.canvasModeAction:
        #     self.canvasModeAction = Krita.instance().action("view_show_canvas_only")
        #     self.selector = next(o for o in Krita.instance().dockers() if o.objectName() == 'ColorSelectorNg')

        # if not self.selector.isFloating():
        #     # 疯狂设置floating可能导致krita卡死，这里定死浮动
        #     self.selector.setFloating(True)
        # if self.selector.isVisible():
        #     self.selector.setVisible(False)
        # else:
        #     pos = QCursor().pos()
        #     self.selector.setVisible(True)
        #     self.selector.setGeometry(int(pos.x() - WIDTH / 2), int(pos.y() - HEIGHT / 2), WIDTH, HEIGHT)
        #     self.selector.repaint()

