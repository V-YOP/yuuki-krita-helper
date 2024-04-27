from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import *
from krita import *
from .constants import *
from .util.Logger import Logger
from .utils import *

TOOLBUTTON_STYLE = """
QToolButton {
    width: 40px;
    height: 40px;
    border: None;
}
QToolButton:checked {
    background-color: #647c91;
}
""".strip()

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
        super().__init__()
        self.logger = Logger()
        self.lastTool: str = None
        self.toolBtns: list[QToolButton] = []
        self.setWindowTitle("My Toolbox")

        item = QWidget(self)
        layout = QVBoxLayout(self)
        def go():
            self.setupLayout(layout)
            item.repaint()
        QTimer.singleShot(0, go)

        item.setLayout(layout)
        self.setWidget(item)
        QTimer.singleShot(0, self.checkCurrentToolLoop)

    def onToolChanged(self, currentTool: str):
        self.logger.info(f"tool changed: {currentTool}")
        for toolBtn in self.toolBtns:
            if toolBtn.objectName() == currentTool:
                self.logger.info(f"checked: {currentTool}")
                toolBtn.setChecked(True)
            else:
                toolBtn.setChecked(False)
            toolBtn.repaint()


    # def currentTool(self):
    #     logger.info('start')
    #     tool = current_tool()
    #     logger.info('end: ' + tool)

    def setupLayout(self, layout: QVBoxLayout):
        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignLeft)
        layout.addLayout(hbox)
        #
        # currentBtn = QPushButton(self)
        # currentBtn.setText("current")
        # currentBtn.clicked.connect(self.currentTool)
        # hbox.addWidget(currentBtn)

        actionToShortCutStr = action_shortcuts()
        for toolName in DISPLAYED_TOOLS:
            iconName = TOOL_NAME_TO_ICON_NAME[toolName]
            btn = QToolButton(self)
            self.toolBtns.append(btn)
            btn.setObjectName(toolName)
            btn.setCheckable(True)
            if toolName in actionToShortCutStr:
                btn.setToolTip(f"#{toolName}: ${actionToShortCutStr[toolName]}")
            else:
                btn.setToolTip(toolName)
            btn.setStyleSheet(TOOLBUTTON_STYLE)
            btn.setIcon(Krita.instance().icon(iconName))
            btn.setIconSize(btn.size())
            def onClick(theToolName):
                def go():
                    set_current_tool(theToolName)
                return go

            btn.clicked.connect(onClick(toolName))
            hbox.addWidget(btn)



    def canvasChanged(self, canvas):
        pass


    def checkCurrentToolLoop(self):
        def go():
            nowTool = current_tool()
            if nowTool is None:
                return
            if nowTool == self.lastTool:
                return
            self.lastTool = nowTool
            self.onToolChanged(nowTool)
        go()
        QTimer.singleShot(33, self.checkCurrentToolLoop)

