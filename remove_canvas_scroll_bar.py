from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QWidget, QAbstractScrollArea

from krita import *
from .util.Logger import Logger


class RemoveCanvasScrollBar(Extension):
    def __init__(self, parent):
        super().__init__(parent)
        self.logger = Logger()
        self.lastActiveView = None
        self.notifier = Krita.instance().notifier()
        self.notifier.imageClosed.connect(lambda _: self.refresh())
        self.notifier.imageCreated.connect(lambda _: self.refresh())
        self.notifier.viewClosed.connect(lambda _: self.refresh())
        self.notifier.viewCreated.connect(lambda _: self.refresh())
        self.notifier.windowCreated.connect(lambda: self.refresh())

    def refresh(self):
        def go():
            self.lastActiveView = None
        QTimer.singleShot(0, go)

    def loop(self):
        def go():
            currentActiveWindow = Krita.instance().activeWindow()
            if currentActiveWindow is None:
                return
            currentActiveView = currentActiveWindow.activeView()
            if currentActiveView is None:
                return
            if self.lastActiveView is not None and currentActiveView == self.lastActiveView:
                return
            self.lastActiveView = currentActiveView
            def magic():
                self.onActiveViewChanged()
                QTimer.singleShot(0, self.onActiveViewChanged)
            QTimer.singleShot(0, self.onActiveViewChanged)
        def mygo():
            go()
            QTimer.singleShot(0, self.loop)
        QTimer.singleShot(33, mygo)

    def onActiveViewChanged(self):
        def go():
            for window in Krita.instance().windows():
                qviews = [i for i in window.qwindow().findChildren(QWidget) if i.metaObject().className() == 'KisView']
                self.logger.info(f"window: {window}, views: {qviews}")
                for qview in qviews:
                    mobj: QAbstractScrollArea = next( (w for w in qview.findChildren(QAbstractScrollArea) if w.metaObject().className() == 'KisCanvasController'), None)
                    self.logger.info(f"{mobj}")
                    mobj.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                    mobj.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        QTimer.singleShot(0, go)

    def setup(self):
        QTimer.singleShot(33, self.loop)
        self.notifier.setActive(True)
        pass

    def createActions(self, window):
        pass

