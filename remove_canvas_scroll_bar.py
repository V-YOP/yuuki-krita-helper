from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QWidget, QAbstractScrollArea

from krita import *
from .util.Logger import Logger


class RemoveCanvasScrollBar(Extension):
    def __init__(self, parent):
        super().__init__(parent)
        self.canvasObjs: list[QAbstractScrollArea] = []
        self.notifier = Krita.instance().notifier()
        self.notifier.imageCreated.connect(lambda _: self.refresh())
        self.notifier.viewCreated.connect(lambda _: self.refresh())

    def refresh(self):
        def go():
            self.canvasObjs = []
            for window in Krita.instance().windows():
                qviews = [i for i in window.qwindow().findChildren(QWidget) if i.metaObject().className() == 'KisView']
                for qview in qviews:
                    mobj: QAbstractScrollArea = next( (w for w in qview.findChildren(QAbstractScrollArea) if w.metaObject().className() == 'KisCanvasController'), None)
                    self.canvasObjs.append(mobj)
        QTimer.singleShot(0, go)

    def loop(self):
        for canvasObj in self.canvasObjs:
            try:
                canvasObj.isVisible() # assert it's not GCed, if so, just ignore it
            except BaseException as e:
                continue
            if canvasObj.verticalScrollBarPolicy() != Qt.ScrollBarAlwaysOff:
                canvasObj.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                canvasObj.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        QTimer.singleShot(33, self.loop)
    def setup(self):
        QTimer.singleShot(33, self.loop)
        self.notifier.setActive(True)
        pass

    def createActions(self, window):
        pass

