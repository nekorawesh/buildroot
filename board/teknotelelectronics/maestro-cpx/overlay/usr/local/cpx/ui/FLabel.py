from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore


class FLabel(QLabel):
    draw_list = []
    label_id = "0"
    label_pre_id = ""
    label_sub_id = ""
    objects = []
    clicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        QLabel.__init__(self, parent)
        self.__class__.objects.append(self)

    @classmethod
    def ekleSil(cls):  # datayı siler
        for obj in cls.objects:
            obj.draw_list = []

    def data_process(self, data):  # append ile ekleme olacak limite ulaşınca sıfırlayacak
        if data <= 7:
            data = [int(char) for char in "{0:03b}".format(data)][::-1]
        else:
            data = [0, 0, 0]

        if len(self.draw_list) == 0:
            self.draw_list = [data]
        elif len(self.draw_list) > 60:
            # self.draw_list = []
            self.draw_list[:-1] = self.draw_list[1:]
            self.draw_list[-1] = data
        else:
            self.draw_list.append(data)
        self.update()

    def refreshData(self):
        self.draw_list = []
        self.update()

    def setData(self, data_list):
        self.draw_list = data_list
        self.update()

    def mousePressEvent(self, event):
        self.clicked.emit()
        super().mousePressEvent(event)

    def paintEvent(self, e):
        super().paintEvent(e)

        pen_color = QtCore.Qt.black
        pen_width = 10
        pen_height = 10
        painter = QtGui.QPainter(self)
        p = painter.pen()
        p.setWidth(pen_width)
        p.setColor(pen_color)
        painter.setPen(p)

        def paintt(draw_list_id, draw_list, start_x: int, start_y: int):
            start_y = start_y + int(pen_width / 2)
            font = QtGui.QFont()
            font.setFamily('Times')
            font.setBold(True)
            font.setPointSize(8)
            # pen_color = QtCore.Qt.black
            pen_color = QtGui.QColor(23, 87, 141)
            p.setColor(pen_color)
            painter.setPen(p)
            painter.setFont(font)

            if draw_list_id == "":
                painter.drawText(start_x - 40, start_y + 13, self.label_id)
            elif self.label_sub_id == "00":
                painter.drawText(start_x + 10, start_y + 13, draw_list_id)

            for line_id in range(len(draw_list)):
                line = draw_list[line_id]
                first_paint_done = False
                total_lights = 0
                for i in line:
                    total_lights += i > 0

                if total_lights > 3:
                    pen_color = QtCore.Qt.red
                    if line[0] == 101:
                        pen_color = QtCore.Qt.darkRed
                    p.setColor(pen_color)
                    if line[0] == 2 or line[0] == 102:
                        p.setWidth(int(pen_width / 2))
                    painter.setPen(p)
                    painter.drawLine(start_x + line_id * pen_width, start_y, start_x + line_id * pen_width,
                                     start_y + pen_height)
                    p.setWidth(pen_width)

                    pen_color = QtCore.Qt.yellow
                    if line[1] == 101:
                        pen_color = QtCore.Qt.darkYellow
                    p.setColor(pen_color)
                    if line[1] == 2 or line[1] == 102:
                        p.setWidth(int(pen_width / 2))
                    painter.setPen(p)
                    painter.drawLine(start_x + line_id * pen_width, start_y + int(pen_height / 3) + int(pen_width / 3),
                                     start_x + line_id * pen_width, start_y + int(pen_height / 3) * 2 + int(pen_width / 3) * 2)
                    p.setWidth(pen_width)

                    pen_color = QtCore.Qt.green
                    if line[2] == 101:
                        pen_color = QtCore.Qt.darkGreen
                    p.setColor(pen_color)
                    if line[2] == 2 or line[2] == 102:
                        p.setWidth(int(pen_width / 2))
                    painter.setPen(p)
                    painter.drawLine(start_x + line_id * pen_width, start_y + int(pen_height / 3) * 2 + int(pen_width / 3) * 2,
                                     start_x + line_id * pen_width, start_y + pen_height)
                    p.setWidth(pen_width)

                else:
                    if line[0] == 1 or line[0] == 101 or line[0] == 2 or line[0] == 102:
                        pen_color = QtCore.Qt.red
                        if line[0] > 100:
                            pen_color = QtCore.Qt.darkRed
                        p.setColor(pen_color)
                        if line[0] == 2 or line[0] == 102:
                            p.setWidth(int(pen_width / 2))
                        painter.setPen(p)
                        if not first_paint_done:
                            painter.drawLine(start_x + line_id * pen_width, start_y, start_x + line_id * pen_width,
                                             start_y + pen_height)
                            first_paint_done = True
                        else:
                            painter.drawLine(start_x + line_id * pen_width, start_y + int(pen_height / 2) + int(pen_width / 2),
                                             start_x + line_id * pen_width, start_y + pen_height)
                        p.setWidth(pen_width)
                        painter.setPen(p)

                    if line[1] == 1 or line[1] == 101 or line[1] == 2 or line[1] == 102:
                        pen_color = QtCore.Qt.yellow
                        if line[1] > 100:
                            pen_color = QtCore.Qt.darkYellow
                        p.setColor(pen_color)
                        if line[1] == 2 or line[1] == 102:
                            p.setWidth(int(pen_width / 2))
                        painter.setPen(p)
                        if not first_paint_done:
                            painter.drawLine(start_x + line_id * pen_width, start_y, start_x + line_id * pen_width,
                                             start_y + pen_height)
                            first_paint_done = True
                        else:
                            painter.drawLine(start_x + line_id * pen_width, start_y + int(pen_height / 2) + int(pen_width / 2),
                                             start_x + line_id * pen_width, start_y + pen_height)
                        p.setWidth(pen_width)
                        painter.setPen(p)

                    if line[2] == 1 or line[2] == 101 or line[2] == 2 or line[2] == 102:
                        pen_color = QtCore.Qt.green
                        if line[2] > 100:
                            pen_color = QtCore.Qt.darkGreen
                        p.setColor(pen_color)
                        if line[2] == 2 or line[2] == 102:
                            p.setWidth(int(pen_width / 2))
                        painter.setPen(p)
                        if not first_paint_done:
                            painter.drawLine(start_x + line_id * pen_width, start_y, start_x + line_id * pen_width,
                                             start_y + pen_height)
                        else:
                            painter.drawLine(start_x + line_id * pen_width, start_y + int(pen_height / 2) + int(pen_width / 2),
                                             start_x + line_id * pen_width, start_y + pen_height)
                        p.setWidth(pen_width)
                        painter.setPen(p)

        if self.label_pre_id == "":
            paintt(self.label_pre_id, self.draw_list, 50, 1)
        else:
            paintt(self.label_pre_id, self.draw_list, 0, 1)


class FLabel_Gprs(QLabel):
    value = 0

    def data_process(self, data):  # append ile ekleme olacak limite ulaşınca sıfırlayacak
        self.value = data
        self.update()

    def paintEvent(self, e):
        super().paintEvent(e)
        pen_width = 2
        start_y = 2
        painter = QtGui.QPainter(self)

        points = QtGui.QPolygon([
            QtCore.QPoint(0 + pen_width / 2, 30 + start_y + pen_width / 2),
            QtCore.QPoint(0 + pen_width / 2, 30 + start_y + pen_width / 2),
            QtCore.QPoint(40 + pen_width / 2, 30 + start_y + pen_width / 2),
            QtCore.QPoint(40 + pen_width / 2, 0 + start_y + pen_width / 2)
        ])

        def paintt(value_percentage):

            painter.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0), 2, QtCore.Qt.NoPen))
            painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0), QtCore.Qt.SolidPattern))

            def gradient(value_percentage, xmin, xmax):
                x_now = (xmax - xmin) * (value_percentage / 100)
                return x_now, (x_now - (xmax - xmin)) / (-2)

            x, y = gradient(value_percentage, 0, 40)
            painter.drawPolygon(QtGui.QPolygon([
                QtCore.QPoint(0 + pen_width / 2, 30 + start_y + pen_width / 2),
                QtCore.QPoint(0 + pen_width / 2, 30 + start_y + pen_width / 2),
                QtCore.QPoint(x + pen_width / 2, 30 + start_y + pen_width / 2),
                QtCore.QPoint(x + pen_width / 2, y + start_y + pen_width / 2)
            ]))
            if value_percentage >= 20:
                painter.setPen(QtGui.QPen(QtGui.QColor(29, 115, 185), 2, QtCore.Qt.SolidLine))
                painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0), QtCore.Qt.NoBrush))
            else:
                painter.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0), 2, QtCore.Qt.SolidLine))
                painter.setBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0), QtCore.Qt.NoBrush))
            painter.drawPolygon(points)

        paintt(self.value)
