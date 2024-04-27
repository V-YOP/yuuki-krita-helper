from typing import Callable, List

from PyQt5.QtCore import qInfo, QTimer
from PyQt5.QtWidgets import QAction

from krita import *


class ActionLoggerExtension(Extension):
    class __IntervalTimer(QTimer):
        def __init__(self, fn: Callable[[QAction, bool], None]):
            super().__init__()
            self.last_states = {}
            self.fn = fn
            self.actions: List[QAction] = []

        def timerEvent(self, a0):
            try:
                for action in self.actions:
                    last_state = self.last_states.get(action.objectName())
                    current_state = action.isChecked()
                    if last_state != current_state:
                        self.fn(action, current_state)
                    self.last_states[action.objectName()] = current_state
            except RuntimeError as e:
                pass

        def set_actions(self, actions: List[QAction]):
            self.actions = actions

    def __init__(self, parent=None):
        self.last_states = {}
        self.timer = self.__IntervalTimer(self.on_action_state_change)
        super().__init__(parent)

    def on_action_state_change(self, action: QAction, state: bool):
        qInfo(f"{action.objectName()}: {state}")
        pass

    def setup(self):
        def go():
            self.timer.set_actions(Krita.instance().actions())
            self.timer.start(33)
        QTimer.singleShot(0, go)
        pass

    def createActions(self, window):
        pass