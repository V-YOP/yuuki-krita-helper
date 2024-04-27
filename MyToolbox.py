from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import *
from krita import *
from .constants import *
from .util.Logger import Logger
from .utils import *

DISPLAYED_TOOLS = [
  'KritaShape/KisToolBrush',
  'KritaFill/KisToolFill',
  'KisToolSelectSimilar',
  'KisToolSelectElliptical',
  'KisToolSelectRectangular',
  'KisToolSelectPolygonal',
  'KisToolSelectOutline',
  'KisToolPolyline',
  'KritaShape/KisToolLazyBrush', # 智能填色（取得什么名字……）
  'KritaShape/KisToolLine',
  'KritaFill/KisToolGradient',
  'ToolReferenceImages',
  'KritaShape/KisToolMeasure',
  'KisAssistantTool',
  'KisToolCrop',
  # 'KisToolEncloseAndFill',
  # 'InteractionTool',
  # 'SvgTextTool',
  # 'KarbonCalligraphyTool',
  # 'PathTool',
  # 'KisToolSelectContiguous',
  # 'KisToolSelectMagnetic', # 磁锁选择
  # 'KisToolSelectPath',
  # 'KisToolPencil',
  # 'KisToolPath',
  # 'KritaShape/KisToolRectangle',
  # 'KritaShape/KisToolEllipse',
  # 'KritaShape/KisToolMultiBrush',
  # 'KritaShape/KisToolDyna',
  # 'KisToolPolygon',
  # 'KritaTransform/KisToolMove',
  # 'KisToolTransform',
  # 'KritaSelected/KisToolColorSampler',
  # 'KritaShape/KisToolSmartPatch',
  # 'ZoomTool',
  # 'PanTool'
]

class MyToolbox(DockWidget):

    def __init__(self):
        self.logger = Logger()
        super().__init__()
        self.setWindowTitle("My Toolbox")

        item = QWidget(self)
        layout = QVBoxLayout(self)
        self.setupLayout(layout)

        item.setLayout(layout)
        self.setWidget(item)
        
    def currentTool(self):
        logger.info('start')
        tool = current_tool()
        logger.info('end: ' + tool)

    def setupLayout(self, layout: QVBoxLayout):
        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignLeft)
        layout.addLayout(hbox)

        currentBtn = QPushButton(self)
        currentBtn.setText("current")
        currentBtn.clicked.connect(self.currentTool)
        hbox.addWidget(currentBtn)

        for toolName in DISPLAYED_TOOLS:
            iconName = TOOL_NAME_TO_ICON_NAME[toolName]
            btn = QToolButton(self)
            btn.setToolTip(toolName)
            btn.setIcon(Krita.instance().icon(iconName))
            def onClick(theToolName):
                def go():
                    set_current_tool(theToolName)
                return go

            btn.clicked.connect(onClick(toolName))
            hbox.addWidget(btn)



    def canvasChanged(self, canvas):
        pass
