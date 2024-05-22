from krita import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

qwindow = Krita.instance().activeWindow().qwindow()
views = Krita.instance().activeWindow().views()

qviews: list[QMdiSubWindow] = qwindow.findChildren(QMdiSubWindow)
print(qviews)
print(views)

def get_view_id(subwin: QMdiSubWindow) -> int:
    view_widget = next((i for i in subwin.findChildren(QWidget) if i.metaObject().className() == 'KisView'), None)
    view_name = view_widget.objectName()
    return int(view_name.replace('view_', ''))

qviews.sort(key=get_view_id)

for qview, view in zip(qviews, views):
    view_id = get_view_id(qview)
    print(f"{qview.windowTitle()=}, {view_id=}, {view.document().name()}")

for qview in qviews:
    qview.setWindowFlag(Qt.WindowStaysOnTopHint)