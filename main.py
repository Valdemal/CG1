from PyQt5.QtCore import QRect, Qt
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtWidgets import QWidget, QApplication

from figures import Cycle, RegularPolygon


class PictureWidget(QWidget):
    MARGIN = 10  # размер отступа внутри окна в пикселях
    MAIN_PEN_THICKNESS = 3  # Толщина основного пера
    SLIM_PEN_THICKNESS = 1  # Толщина тонкого пера
    ANGLES_COUNT = 10  # Количество углов вписанных многоугольгиков

    def __init__(self, width: int, height: int, title: str):
        QWidget.__init__(self)

        self.resize(width, height)
        self.setWindowTitle(title)
        self.__init_figures()

    def __init_figures(self):
        self.__cycle = Cycle(inner_color=Qt.red)
        self.__big_polygon = RegularPolygon(self.ANGLES_COUNT, inner_color=Qt.gray)
        self.__small_polygon = RegularPolygon(self.ANGLES_COUNT, inner_color=Qt.white)

        # Внимание!!! Добавление фигур в порядке отрисовки
        self.__figures = [self.__cycle, self.__big_polygon, self.__small_polygon]

    def paintEvent(self, event) -> None:
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)  # Включение сглаживания

        draw_rect: QRect = event.rect()
        draw_rect.setCoords(
            self.MARGIN, self.MARGIN,
            self.width() - self.MARGIN, self.height() - self.MARGIN
        )

        self.__update_figures(draw_rect)
        self.draw(painter)

        painter.end()

    def draw(self, painter: QPainter):

        for figure in self.__figures:
            figure.draw(painter)

        self.__draw_lines_between_polygons(painter)

    def __update_figures(self, draw_rect: QRect):

        for figure in self.__figures:
            figure.center = draw_rect.center()

        self.__big_polygon.center_distance = self.__cycle.radius = min(draw_rect.height() / 2, draw_rect.width() / 2)
        self.__small_polygon.center_distance = self.__big_polygon.center_distance / 4

    def __draw_lines_between_polygons(self, painter: QPainter):
        painter.setPen(QPen(QBrush(Qt.black), self.SLIM_PEN_THICKNESS))

        big_polygon_points = self.__big_polygon.get_points()
        small_polygon_points = self.__small_polygon.get_points()

        for i in range(self.ANGLES_COUNT - 1):
            painter.drawLine(small_polygon_points[i], big_polygon_points[i + 1])

        painter.drawLine(small_polygon_points[len(small_polygon_points) - 1], big_polygon_points[0])


if __name__ == '__main__':
    app = QApplication([])

    widget = PictureWidget(600, 400, 'Лабораторная работа №1')

    widget.show()
    app.exec_()
