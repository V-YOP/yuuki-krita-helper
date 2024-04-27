from dataclasses import dataclass
from krita import *
from .utils import *
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
