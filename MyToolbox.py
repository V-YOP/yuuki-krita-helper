
from krita import *
from .constants import *
from .util.Logger import Logger
from .utils import *

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import *

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
  'KritaShape/KisToolLazyBrush', # 智能填色（取得什么名字……）
  'KisToolSelectElliptical',
  'KisToolSelectRectangular',
  'KisToolSelectPolygonal',
  'KisToolSelectOutline',
  'KisToolPolyline',
  'KritaShape/KisToolLine',
  'KritaFill/KisToolGradient',
  'ToolReferenceImages',
  'KisToolCrop',
  'KritaShape/KisToolMeasure',
  'KisAssistantTool',
  'SvgTextTool',
  # 'KisToolEncloseAndFill',
  # 'InteractionTool',
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
        self.saveFloatingLayoutAction: QAction = None
        self.toggleFloatingDockerToolbarAction: QAction = None
        def go():
            self.saveFloatingLayoutAction = Krita.instance().action('pykrita_yuuki_krita_helper_save_floating_docker')
            self.toggleFloatingDockerToolbarAction = Krita.instance().action('pykrita_yuuki_krita_helper_toggle_floating_docker_toolbar')
            layout.addLayout(self.toolbox_line())

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

    def toolbox_line(self):
        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignLeft)
        #
        # currentBtn = QPushButton(self)
        # currentBtn.setText("current")
        # currentBtn.clicked.connect(self.currentTool)
        # hbox.addWidget(currentBtn)

        btn = QToolButton(self)
        btn.setText('S')
        btn.setToolTip('save floating layout')
        btn.clicked.connect(self.saveFloatingLayoutAction.trigger)
        hbox.addWidget(btn)

        btn = QToolButton(self)
        btn.setText('T')
        btn.setToolTip('toggle floating docker title bars')
        btn.clicked.connect(self.toggleFloatingDockerToolbarAction.trigger)
        hbox.addWidget(btn)

        ### add
        split0 = QLabel(self)
        split0.setText('|')
        hbox.addWidget(split0)

        ### add tools
        actionToShortCutStr = action_shortcuts()
        for toolName in DISPLAYED_TOOLS:
            iconName = TOOL_NAME_TO_ICON_NAME[toolName]
            btn = QToolButton(self)
            self.toolBtns.append(btn)
            btn.setObjectName(toolName)
            btn.setCheckable(True)
            if toolName in actionToShortCutStr:
                btn.setToolTip(f"#{toolName} ({actionToShortCutStr[toolName]})")
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

        split1 = QLabel(self)
        split1.setText('|')
        hbox.addWidget(split1)

        edit_time_label = QLabel(self)
        hbox.addWidget(edit_time_label)
        edit_time_label.setText('00:00:00')
        self.loop_update_document_edit_time(edit_time_label)


        # btn = QToolButton(self)
        # btn.setText('hello')
        # hbox.addWidget(btn)
        return hbox


    def loop_update_document_edit_time(self, label: QLabel):
        def biz(document: Document | None):
            if document is None:
                return
            
            edit_time = DocumentInfo.from_document(document).edit_time
            hour = str(edit_time // 3600).rjust(2, '0')
            minute = str((edit_time % 3600) // 60).rjust(2, '0')
            second = str(edit_time % 60).rjust(2, '0')
            label.setText(f"{hour}:{minute}:{second}")

        def go():
            biz(active_document())
            QTimer.singleShot(1000, go)
        go()

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
        QTimer.singleShot(66, self.checkCurrentToolLoop)

