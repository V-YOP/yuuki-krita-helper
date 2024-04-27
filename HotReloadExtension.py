# from krita import *
import datetime
from types import ModuleType
from typing import Type, List

from PyQt5.QtCore import QTimer

from .util.Logger import Logger
import inspect

from .IntervalTask import IntervalTask
from krita import *


class HotReloadExtension(Extension):
    class __HotReloader:
        __instance = None

        def __new__(cls):
            if cls.__instance is None:
                cls.__instance = super().__new__(cls)
            return cls.__instance

        def __init__(self):
            self.__logger = Logger()
            # module -> instances
            self.__module2instances: dict[ModuleType, List["HotReloadExtension"]] = {}
            self.__module2last_modify_time: dict[ModuleType, str] = {}
            self.__reload_module_task = IntervalTask(lambda _: self.__reload_module(), 500)
            self.__timer = QTimer()
            self.__reload_module_task.start(self.__timer)

        def __reload_module(self):
            for module, inses in self.__module2instances.items():
                # build class 2 instances map
                class2instances = {}
                for instance in inses:
                    class2instances.setdefault(type(instance), [])
                    class2instances[type(instance)].append(instance)
                for classType, instances in class2instances.items():

                    locals_ = {}
                    try:
                        source = inspect.getsource(classType)
                        exec(source, module.__dict__, locals_)
                        new_class_type = locals_[classType.__name__]
                    except Exception as e:
                        return

                    for instance in instances:
                        instance.__class__ = new_class_type

        def register(self, instance: "HotReloadExtension"):
            childModule = inspect.getmodule(type(instance))
            self.__logger.info(f"HotReloadExtension inited, class: {type(instance)}, defined file: {childModule}")
            self.__module2instances.setdefault(childModule, [])
            self.__module2instances[childModule].append(instance)

    __hot_reloader = __HotReloader()

    def __init__(self, parent):
        super().__init__(parent)
        childClass = type(self)
        if childClass == HotReloadExtension:
            # do nothing if not inherited
            return
        self.__hot_reloader.register(self)
