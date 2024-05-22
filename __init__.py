from .freeze_popup_palette_size import FreezePopupPaletteSize
from .toolbar_modifier import ToolbarModifier
from .action_logger_extension import ActionLoggerExtension
from .yuuki_krita_helper import Yuuki_krita_helper
from .krita_status_watcher import *
from .floating_docker_helper import *
from .view_helper_extension import *
from .MyToolbox import *

# And add the extension to Krita's list of extensions:
app = Krita.instance()
# Instantiate your class:
app.addExtension(Yuuki_krita_helper(parent=app))
app.addExtension(Krita_status_watcher(parent=app))
app.addExtension(ActionLoggerExtension(parent=app))
app.addExtension(ToolbarModifier(parent=app))
app.addExtension(FreezePopupPaletteSize(parent=app))
app.addExtension(FloatingDockerHelper(parent=app))
app.addExtension(ViewHelperExtension(parent=app))

Krita.instance().addDockWidgetFactory(DockWidgetFactory("MyToolbox", DockWidgetFactoryBase.DockRight, MyToolbox))
