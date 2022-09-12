from abc import ABC, abstractmethod
from math import cos, pi, sin
from typing import List

from PyQt5.QtCore import QPointF, Qt, QLineF
from PyQt5.QtGui import QPainter, QBrush, QPen, QPainterPath


class Drawable(ABC):

    @abstractmethod
    def draw(self, painter: QPainter):
        pass

    # @abstractmethod
    # def rotate(self, angle_in_degrees: float):
    #     pass


# Создать компоновщика

class Figure(Drawable):
    def __init__(self, center: QPointF = QPointF(0, 0),
                 border_color=Qt.black,
                 inner_color=Qt.white,
                 border_thickness: int = 3):
        self.__center = center
        self.__border_color = border_color
        self.__inner_color = inner_color
        self.__border_thickness = border_thickness

    @property
    def center(self) -> QPointF:
        return self.__center

    @center.setter
    def center(self, value: QPointF):
        self.__center = value

    @property
    def inner_color(self):
        return self.__inner_color

    @inner_color.setter
    def inner_color(self, value):
        self.__inner_color = value

    @property
    def border_color(self):
        return self.__border_color

    @border_color.setter
    def border_color(self, value):
        self.__border_color = value

    @property
    def border_thickness(self) -> int:
        return self.__border_thickness

    @border_thickness.setter
    def border_thickness(self, value: int):
        self.__border_thickness = value

    def draw(self, painter: QPainter):
        painter.setPen(QPen(QBrush(self.__border_color), self.__border_thickness))
        painter.setBrush(QBrush(self.__inner_color))


class Cycle(Figure):
    def __init__(self, radius: float = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__radius = radius

    @property
    def radius(self) -> float:
        return self.__radius

    @radius.setter
    def radius(self, value: float):
        self.__radius = value

    def draw(self, painter: QPainter):
        super(Cycle, self).draw(painter)
        painter.drawEllipse(self.center, self.radius, self.radius)


class RegularPolygon(Figure):
    def __init__(self, sides_count: int, center_distance: float = 0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__sides_count = sides_count
        self.__center_distance = center_distance
        self.__init_points()

    def __init_points(self):
        pi2 = 2 * pi
        self.__points = [
            QPointF(
                self.center.x() + self.center_distance * cos(pi2 * i / self.sides_count),
                self.center.y() + self.center_distance * sin(pi2 * i / self.sides_count),
            ) for i in range(self.sides_count)
        ]

    @property
    def center_distance(self) -> float:
        return self.__center_distance

    @center_distance.setter
    def center_distance(self, value: float):
        self.__center_distance = value
        self.__init_points()

    @property
    def sides_count(self) -> int:
        return self.__sides_count

    def get_points(self) -> List[QPointF]:
        return self.__points

    def draw(self, painter: QPainter):
        super().draw(painter)

        path = QPainterPath()
        path.moveTo(self.__points[0])
        for i in range(1, len(self.__points)):
            path.lineTo(self.__points[i])
            painter.drawLine(self.__points[i-1], self.__points[i])

        painter.drawLine(self.__points[len(self.__points) - 1], self.__points[0])
        path.lineTo(self.__points[0])
        painter.fillPath(path, QBrush(self.inner_color))


    @Figure.center.setter
    def center(self, value: QPointF):
        Figure.center.fset(self, value)
        self.__init_points()
