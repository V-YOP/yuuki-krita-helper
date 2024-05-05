from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QWidget, QAbstractScrollArea

from krita import *
from .util.Logger import Logger


class FreezePopupPaletteSize(Extension):
    def __init__(self, parent):
        super().__init__(parent)
        self.logger = Logger()
        self.notifier = Krita.instance().notifier()
        self.onConfigurationChanged()
        self.notifier.configurationChanged.connect(self.onConfigurationChanged)

    def onConfigurationChanged(self):
        self.logger.info('configuration changed, reset popup palette size')
        Krita.instance().writeSetting('', 'popuppalette/selectorSize', '500')
        Krita.instance().writeSetting('', 'popuppalette/size', '800')

    def setup(self):
        # QTimer.singleShot(66, self.loop)
        self.notifier.setActive(True)
        pass

    def createActions(self, window):
        pass

