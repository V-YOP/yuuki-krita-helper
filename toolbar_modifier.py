from PyQt5.QtWidgets import QWidget, QLayout, QVBoxLayout

from krita import *
from .IntervalTask import *
from .util.Logger import Logger

logger = Logger()

DISPLAYED_TOOLS = {
  # 'InteractionTool',
  # 'SvgTextTool',
  # 'KarbonCalligraphyTool',
  # 'PathTool',
  # 'KisToolSelectContiguous',
  'KisToolSelectOutline',
  # 'KisToolSelectMagnetic', # 磁锁选择
  'KisToolSelectRectangular',
  'KisToolSelectPolygonal',
  # 'KisToolSelectPath',
  'KisToolSelectSimilar',
  'KisToolSelectElliptical',
  # 'KisToolPencil',
  'KritaShape/KisToolBrush',
  # 'KisToolPath',
  # 'KritaShape/KisToolRectangle',
  'KisToolPolyline',
  # 'KritaShape/KisToolEllipse',
  'KritaShape/KisToolLine',
  # 'KritaShape/KisToolMultiBrush',
  # 'KritaShape/KisToolDyna',
  # 'KisToolPolygon',
  # 'KritaTransform/KisToolMove',
  'KisToolCrop',
  # 'KisToolTransform',
  'KritaShape/KisToolLazyBrush', # 智能填色（取得什么名字……）
  'KisToolEncloseAndFill',
  # 'KritaSelected/KisToolColorSampler',
  # 'KritaShape/KisToolSmartPatch',
  'KritaFill/KisToolFill',
  'KritaFill/KisToolGradient',
  'KisAssistantTool',
  'ToolReferenceImages',
  'KritaShape/KisToolMeasure',
  # 'ZoomTool',
  # 'PanTool'
}

class ToolbarModifier(Extension):
    def __init__(self, parent):
        super().__init__(parent)
        self.tasks: list[IntervalTask] = [
            # IntervalTask(lambda e: self.knife_mode_loop(), 33),
            IntervalTask(lambda e: self.modify_toolbar(), 1000)
        ]

    def modify_toolbar(self):
        try:
            qdock = next((w for w in Krita.instance().dockers() if w.objectName() == 'ToolBox'), None)
            pobj = qdock.findChild(QWidget, 'qt_scrollarea_viewport')
            mobj = next((w for w in pobj.findChildren(QWidget) if w.metaObject().className() == 'KoToolBox'), None)
            children: list[QToolButton] = mobj.findChildren(QToolButton)
            for child in children:
                if child.objectName() not in DISPLAYED_TOOLS:
                    child.setVisible(False)
        except BaseException as e:
            pass

    def setup(self):
        for task in self.tasks:
            task.start(self)

    def createActions(self, window):
        pass

