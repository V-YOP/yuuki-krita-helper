from .remove_canvas_scroll_bar import RemoveCanvasScrollBar
from .toolbar_modifier import ToolbarModifier
from .action_logger_extension import ActionLoggerExtension
from .yuuki_krita_helper import Yuuki_krita_helper
from .krita_status_watcher import *
# And add the extension to Krita's list of extensions:
app = Krita.instance()
# Instantiate your class:
app.addExtension(Yuuki_krita_helper(parent=app))
app.addExtension(Krita_status_watcher(parent=app))
app.addExtension(ActionLoggerExtension(parent=app))
app.addExtension(ToolbarModifier(parent=app))
app.addExtension(RemoveCanvasScrollBar(parent=app))
