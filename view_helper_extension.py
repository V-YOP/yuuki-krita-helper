"""
在view下添加菜单：

1. Add Overview：新增一个显示当前文档的始终置顶的视图
2. Minimize All：最小化所有视图
3. Close Duplicate Views：关闭每个文档的重复view，优先关闭浮动的view


"""
from typing import Tuple
from .utils import *
from krita import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

EXTENSION_ID = 'view_helper_extension'

class ViewHelperExtension(Extension):
    @staticmethod
    def all_views(window: Window) -> list[Tuple[int, QMdiSubWindow, View]]:
        qwindow = window.qwindow()
        views = window.views()
        if views is None:
            return []
        qviews: list[QMdiSubWindow] = qwindow.findChildren(QMdiSubWindow)
        def get_view_id(subwin: QMdiSubWindow) -> int:
            view_widget = next((i for i in subwin.findChildren(QWidget) if i.metaObject().className() == 'KisView'), None)
            view_name = view_widget.objectName()
            return int(view_name.replace('view_', ''))

        qviews.sort(key=get_view_id)

        res = []
        for qview, view in zip(qviews, views):
            view_id = get_view_id(qview)
            res.append((view_id, qview, view))
        return res

    def __init__(self, parent):
        super().__init__(parent)
        self.notifier = Krita.instance().notifier()
        self.frameless_add_overview_action: QAction = None
        self.minimize_all_action: QAction = None
        self.frameless_view_action: QAction = None
        pass

    def setup(self):
        # def go(view: View):
        #     if not self.frameless_view_action:
        #         return
        #     self.set_all_views_frameless(view.window(), self.frameless_view_action.isChecked())
        # self.notifier.viewCreated.connect(go)
        self.notifier.setActive(True)
        pass

    def createActions(self, window):
        
        self.add_overview_action = window.createAction(EXTENSION_ID + "_add_overview",
                                                                    "Add Overview View",
                                                                    "tools")
        
        self.add_overview_action.triggered.connect(self.add_overview)

        self.minimize_all_action = window.createAction(EXTENSION_ID + "_minimize_all",
                                                                    "Minimize All Views",
                                                                    "tools")
        
        self.minimize_all_action.triggered.connect(self.minimize_all_views)

        self.minimize_all_action = window.createAction(EXTENSION_ID + "_close_duplicate_views",
                                                                    "Close Duplicate Views",
                                                                    "tools")
        
        self.minimize_all_action.triggered.connect(self.close_duplicate_views)
        
        # self.frameless_view_action = window.createAction(EXTENSION_ID + "_frameless_view",
        #                                                             "Frameless Views",
        #                                                              "tools")
        # self.frameless_view_action.setCheckable(True)
        # self.frameless_view_action.setChecked(False)
        # self.frameless_view_action.triggered.connect(lambda: self.set_all_views_frameless(active_window(), self.frameless_view_action.isChecked()))

    def minimize_all_views(self):
        all_views = ViewHelperExtension.all_views(active_window())
        for _, qview, _ in all_views:
            qview.showMinimized()

    def close_duplicate_views(self):
        all_views = ViewHelperExtension.all_views(active_window())
        all_views.sort(key=lambda x: not x[1].isMaximized())
        

        id_set: set[str] = set()
        for _, qview, view in all_views:
            if view.document().rootNode().uniqueId() in id_set:
                qview.close()
                continue
            id_set.add(view.document().rootNode().uniqueId())


    def set_all_views_frameless(self, window: Window, frameless = True):
        all_views = ViewHelperExtension.all_views(window)
        for _, qview, _ in all_views:
            qview.setWindowFlag(Qt.FramelessWindowHint, frameless)

    def add_overview(self):
        document = active_document()
        if document is None:
            floating_message("no active document!", priority=0, timeout=1000)
            return
        window = active_window()
        window.addView(document)
        # all_views = ViewHelperExtension.all_views(window)
        def go():  
            neo_all_views = ViewHelperExtension.all_views(window)
            _, qview, view = neo_all_views[-1]
            qview.setWindowFlag(Qt.WindowStaysOnTopHint, True)
            qview.showNormal()
            geo = qview.geometry()
            geo.setWidth(400)
            geo.setHeight(420)
            qview.setGeometry(geo)
            
        QTimer.singleShot(0, go)
            
