from dataclasses import dataclass
from typing import Callable

from PyQt5.QtCore import QTimerEvent, QTimer, QObject
from .KritaState import *


@dataclass
class IntervalTask:
    fn: Callable[[QTimerEvent], None]
    interval: int

    class __IntervalTimer(QTimer):
        def __init__(self, parent: QObject, fn):
            super().__init__(parent)
            self.fn = fn

        def timerEvent(self, a0):
            self.fn(a0)

    @staticmethod
    def watch_state_task(fn: Callable[[KritaState, KritaState], None], interval: int):
        last_state = KritaState.fetch()

        def task(e: QTimerEvent):
            nonlocal last_state
            if not active_window():
                return
            new_state = KritaState.fetch()
            if last_state is not None and new_state is not None:
                fn(last_state, new_state)
            last_state = new_state

        return IntervalTask(task, interval)

    logger = Logger("draw time counter")

    @staticmethod
    def draw_time_count_task(fn: Callable[[DocumentInfo, DocumentInfo], None], interval: int):
        def get_document_info() -> None | DocumentInfo:
            document = active_document()
            if document is None:
                return None
            return DocumentInfo.from_document(document)

        last_document_info = get_document_info()

        def task(e: QTimerEvent):
            nonlocal last_document_info
            logger.info("start recording current painting status")
            current_document_info = get_document_info()
            if current_document_info is not None and last_document_info is not None and current_document_info.id == last_document_info.id:
                logger.info(f"title: {last_document_info.title}, create_time: {last_document_info.create_date}, last_edit_time: {last_document_info.edit_time} s, current_edit_time: {current_document_info.edit_time} s")
                fn(last_document_info, current_document_info)
            else:
                logger.info("not same document against last recording, aborted")
            last_document_info = current_document_info

        return IntervalTask(task, interval)



    def start(self, parent: QObject):
        timer = self.__IntervalTimer(parent, self.fn)
        timer.start(self.interval)
