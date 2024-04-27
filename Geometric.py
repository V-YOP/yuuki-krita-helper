from dataclasses import dataclass
from typing import Union

@dataclass
class Point:
    x: int
    y: int

    def distance(self, target: Union["Point", "Line"]) -> float:
        """
        distance to a point or a line
        :param target: point or line object
        :return: distance to target
        """
        pass


@dataclass
class Line:
    start: Point
    end: Point

    def interact(self, line: "Line") -> Point | None:
        pass

