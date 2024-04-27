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

class Yuuki_krita_helper(Extension):

    def __init__(self, parent):
        super().__init__(parent)
        self.last_selection = None
        self.toggle_knife_mode: QAction | None = None
        self.tools = None
        self.last_call_time = None
        self.selector = None
        # self.canvasModeAction = None

        self.tasks: list[IntervalTask] = [
            # IntervalTask(lambda e: self.knife_mode_loop(), 33),
            # IntervalTask(lambda e: self.removeScrollBar(), 33)
        ]

    def removeScrollBar(self):
        if Krita.instance().activeDocument() is None:
            return
        activeWindow = Krita.instance().activeWindow()
        if activeWindow is None:
            return
        qwin = activeWindow.qwindow()
        pobj = qwin.findChild(QWidget, 'view_0')
        if pobj is None:
            return
        mobj: QAbstractScrollArea = next(
            (w for w in pobj.findChildren(QAbstractScrollArea) if w.metaObject().className() == 'KisCanvasController'),
            None)
        if mobj is None:
            return
        def go():
            mobj.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            mobj.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        go()
        # QTimer.singleShot(0, go)


    def setup(self):
        for task in self.tasks:
            task.start(self)

    # TODO 重做时如何处理gc
    # @timemeter
    def knife_mode_loop(self):
        try:
            if not self.toggle_knife_mode or not self.toggle_knife_mode.isChecked():
                return
            document = active_document()
            if not document:
                return
            selection = document.selection()
            if not selection or selection.width() == 0 or selection.height() == 0:
                return

            Krita.instance().action("fill_selection_foreground_color").trigger()
            # document.waitForDone()
            document.setSelection(None)
        except BaseException as e:
            pass

    refs = []

    def createActions(self, window):
        pass
        # status = window.createAction(EXTENSION_ID + "status_", "status", "tools")


        # self.toggle_knife_mode = window.createAction(EXTENSION_ID + "_toggle_knife_mode", "Toggle Knife Mode", "tools")
        # self.toggle_knife_mode.setCheckable(True)
        # self.toggle_knife_mode.setChecked(False)

    def tool_binding(self):
        if not self.tools:
            self.tools: list[QToolButton] = find_tool_box().findChildren(QToolButton)

        def tool_fn(tool: QToolButton):
            def go():
                logger.info(f"{tool.objectName()}: {'active' if tool.isChecked() else 'inactive'}")
            return go

        for tool in self.tools:
            fn = tool_fn(tool)
            tool.toggled.connect(fn)

    def status(self):
        #
        logger.info(f"{DocumentInfo.from_document(active_document()).id}")
        # # tools: list[QToolButton] = find_tool_box().findChildren(QToolButton)
        # # brush = next(tool for tool in tools if tool.objectName() == 'KritaShape/KisToolBrush')
        # # logger.info(f"{[c.objectName() for c in find_tool_box().children()]}")
        # # brush.hide()
        # # logger.info(f"{DocumentInfo.from_document(active_document())}")
        # logger.info(f"{[n.name() for n in active_document().topLevelNodes()]}")
        # logger.info(f"{active_document().rootNode().name()} {active_document().rootNode().objectName()}")
        # active_document().rootNode().setName("rrrrrr")
        # logger.info(f"{active_document().rootNode().name()} {active_document().rootNode().objectName()}")
        # active_document().save()
        # logger.info(f"{active_document().topLevelNodes()[3].property('hello')}")
        #
        # logger.info(f"{active_document().topLevelNodes()[3].setProperty('hello', 'world')}")
        # logger.info(f"{active_document().topLevelNodes()[3].property('hello')}")
        box = QMessageBox()
        box.setText("??")
        # box.__SELF__ = box
        box.open()
        # self.refs.append(box)
