import os
import sys
import time
from typing import Callable, Optional

from PyQt5.QtCore import QTimer, QTimerEvent, QObject

from .util.Logger import Logger
from .utils import floating_message, DocumentInfo
from .IntervalTask import IntervalTask
from .KritaState import KritaState
from krita import *
from datetime import datetime
logger = Logger()

RECORD_INTERVAL = 180

class Krita_status_watcher(Extension):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tasks = [
            IntervalTask.watch_state_task(self.on_eraser_mode_change, 33),
            IntervalTask.draw_time_count_task(self.record_draw_time, RECORD_INTERVAL * 1000),
        ]
        os.makedirs(os.path.join(os.path.expanduser("~"), ".kra_history"), exist_ok=True)
        self.log_file = open(os.path.join(os.path.expanduser("~"), ".kra_history", "history"), 'a')

    def on_eraser_mode_change(self, old: KritaState, new: KritaState):
        if old.eraser_mode != new.eraser_mode:
            state = "ON" if new.eraser_mode else "OFF"
            floating_message(f"eraser mode: {state}")

    def record_draw_time(self, old: DocumentInfo, new: DocumentInfo):
        if old.edit_time == new.edit_time:
            logger.info("no difference, skipped")
            return
        diff = new.edit_time - old.edit_time
        if diff > RECORD_INTERVAL:
            diff = RECORD_INTERVAL
        now = datetime.now()
        logger.info(f"time: {now.strftime('%Y-%m-%d %H:%M:%S')}, file_name: {new.document.fileName()}, id: {new.id}, diff: {diff} s")
        self.log_file.write("##".join(map(str, [now.strftime("%Y-%m-%d %H:%M:%S"), new.document.fileName(), new.id, diff])) + "\n")
        self.log_file.flush()


    def setup(self):
        [task.start(self) for task in self.tasks]

    def createActions(self, window):
        pass
