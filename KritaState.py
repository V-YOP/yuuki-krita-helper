from dataclasses import dataclass
from typing import Any, Generic, TypeVar
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from krita import *
from .utils import *
from .util.Logger import Logger
from datetime import datetime


@dataclass
class KritaState:
    eraser_mode: bool
    current_tool: str

    @staticmethod
    def fetch() -> Optional["KritaState"]:
        document = active_document()
        if not document:
            return None
        eraser_mode = Krita.instance().action("erase_action").isChecked()
        return KritaState(eraser_mode, "")

class HashedWindow:
    def __init__(self, window: Window) -> None:
        self.window = window
    def __hash__(self) -> int:
        return hash(self.window.qwindow().objectName())
    def __eq__(self, other: object) -> bool:
        return isinstance(other, HashedWindow) and self.window.qwindow().objectName() == other.window.qwindow().objectName()

# T = TypeVar('T') 
# class MyKritaState(Generic[T]):
#     @staticmethod
#     def __default_comparator(value1, value2):
#         if value1 is None and value2 is None:
#             return True
#         elif value1 is None or value2 is None:
#             return False
#         elif isinstance(value1, (int, float, str)):
#             return value1 == value2
#         else:
#             return value1 is value2

#     def __init__(self, 
#                  name: str,
#                  state_resolver: Callable[[Callable[[Window, T] , None]], None], 
#                  setter: Callable[[Window, str], None] = None,
#                  comparator: Callable[[T, T], bool] = None) -> None:
#         self.states: dict[HashedWindow, T] = {}
#         self.cbs: list[Callable[[Window, T, T], None]] = []
#         self.setter = setter
#         self.name = name
#         self.logger = Logger(self.name)
#         self.comparator = comparator if comparator is not None else self.__default_comparator
#         state_resolver(self.__state_changed)
#         self.notifier = Krita.instance().notifier()
#         self.notifier.active()
#         self.notifier.windowIsBeingCreated.connect(self.__on_windows_created)
    
#     def __on_windows_created(self, window: Window):
#         def go():
#             self.states.pop(HashedWindow(window), None)

#         window.windowClosed.connect(go)

#     def __state_changed(self, window: Window, state: T):
#         old_state = self.get(window)
#         if self.comparator(old_state, state):
#             return
#         self.logger.info(f"{window.qwindow().objectName()}: state changed from {old_state} to {state}")
#         for cb in self.cbs:
#             cb(window, old_state, state)
#         self.states[HashedWindow(window)] = state

#     def get(self, window: Window = None) -> Optional[T]:
#         window = Krita.instance().activeWindow() if window is None else window
#         if window is None:
#             raise Exception(f"{self.name}: No active window")
#         return self.states.get(HashedWindow(window))
    
#     def set(self, state: str, window: Window = None):
#         if self.setter is None:
#             raise Exception(f"{self.name}: setter is not given!")
#         window = Krita.instance().activeWindow() if window is None else window
#         if window is None:
#             raise Exception(f"{self.name}: No active window")
#         self.setter(window, state)

#     def on_state_changed(self, cb: Callable[[Window, T, T], None]):
#         self.cbs.append(cb)

# class IntervalKritaState(MyKritaState[T]):
#     def __init__(self, 
#                  name: str,
#                  state_getter: Callable[[Window], T], 
#                  ms: int, 
#                  setter: Callable[[Window, str], None] = None,
#                  comparator: Callable[[T, T], bool] = None,
#                  only_active_window = True) -> None:
        
#         def go(resolve):
#             if only_active_window:
#                 if window := Krita.instance().activeWindow():
#                     state = state_getter(window)
#                     resolve(window, state)
#             else:
#                 for window in Krita.instance().windows():
#                     state = state_getter(window)
#                     resolve(window, state)
#             QTimer.singleShot(ms, lambda: go(resolve))
#         super().__init__(name, go, setter, comparator)

# class CurrentToolStateGetter:
#     def __init__(self) -> None:    
#         self.__toolbox_buttons: dict[HashedWindow, list[QToolButton]] = {}
#         self.logger = Logger()

#     def __find_tool_box(self, window: Window) -> Optional[QWidget]:
#         qwindow = window.qwindow()
#         for qobj in qwindow.findChildren(QObject):
#             if qobj.metaObject().className() == "KoToolBox":
#                 return qobj
        
#     def __get_toolbox_buttons(self, window: Window) -> list[QToolButton]:
#         cache = self.__toolbox_buttons.get(HashedWindow(window))
#         if cache is not None and len(cache) != 0:
#             return cache
#         tool_box = self.__find_tool_box(window)
#         if tool_box is None:
#             return []
#         res = tool_box.findChildren(QToolButton)
#         if len(res) == 0:
#             return []
#         self.__toolbox_buttons[HashedWindow(window)] = res
#         return res

#     def __current_tool(self, window: Window) -> Optional[QToolButton]:
#         btns = self.__get_toolbox_buttons(window)
#         if btns is None or len(btns) == 0:
#             return None
#         for btn in btns:
#             try:
#                 if btn.isChecked():
#                     return btn
#             except BaseException as e:
#                 return None
#         return None
        
#     def __call__(self, window: Window) -> Optional[QToolButton]:
#         return self.__current_tool(window)

# current_tool_state = IntervalKritaState(
#     'current_tool', 
#     CurrentToolStateGetter(), 
#     33)
# logger = Logger('current tool')
# current_tool_state.on_state_changed(lambda w, old, neo: logger.info(f"{w.qwindow().objectName()}: ${None if old is None else old.objectName()} -> ${neo.objectName()}"))