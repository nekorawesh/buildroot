from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt, QSize

from FHBoxLayout import duration_h_boxes, edit_buttons, duration_labels
from FLabel import FLabel
from hssMessages import button_width, min_duration_h_box_width, h_box_total_min_size, signal_sequence, \
    selected_sequence

button_style_sheet = """
QPushButton {
    background-color: rgb(23, 87, 141);
    color: rgb(255, 255, 255);
    border-radius: 10px;
    max-width: """ + str(button_width) + """px;
    min-width: """ + str(button_width) + """px;
}
QPushButton:hover {
    background-color: rgb(29, 115, 185);
}
QPushButton:pressed {
    background-color: rgb(35, 135, 217);
    color: rgb(0, 0, 0);
}
"""

label_style_sheet = """
color: rgb(23, 87, 141);
border-bottom: 2px solid;
border-bottom-color: rgb(23, 87, 141);
border-style: outset;"""

label_id_style_sheet = label_style_sheet + """
border-left: 2px solid;
border-left-color: rgb(23, 87, 141);"""

# This is an array that will keep the references to all the labels
# in a 2D array. For example: labels[3][2] will refer to .._loop_03_02
labels = {}

edit_clicked = [False]


def reset_labels():
    for i in range(len(labels[selected_sequence[0]])):
        for j in range(len(labels[selected_sequence[0]][i])):
            labels[selected_sequence[0]][i].pop(0).deleteLater()


def get_label(line, row) -> FLabel:
    return labels[selected_sequence[0]][line][row]


def insert_label(label, line, row):
    if selected_sequence[0] not in labels:
        labels[selected_sequence[0]] = []

    line_dif = line - len(labels[selected_sequence[0]])
    if line_dif > 0:
        for _ in range(line_dif):
            labels[selected_sequence[0]].append([None])

    row_dif = row - len(labels[selected_sequence[0]][line - 1])
    if row_dif > 0:
        for _ in range(row_dif):
            labels[selected_sequence[0]][line - 1].append(None)

    labels[selected_sequence[0]][line - 1][row - 1] = label


def refresh_data_in_all_labels():
    for i in range(len(labels[selected_sequence[0]])):
        for j in range(len(labels[selected_sequence[0]][i])):
            duration = signal_sequence[selected_sequence[0]][j].duration
            if duration < h_box_total_min_size / 10:
                duration = h_box_total_min_size / 10
            if j < len(signal_sequence[selected_sequence[0]]) and i < len(signal_sequence[selected_sequence[0]][j].lights):
                get_label(i, j).setData([signal_sequence[selected_sequence[0]][j].lights[i] for _ in range(int(duration))])
            get_label(i, j).setMinimumSize(duration * 10, 25)
            get_label(i, j).setMaximumSize(duration * 10, 25)


def refresh_data_in_label(index):
    for i in range(len(labels[selected_sequence[0]])):
        duration = signal_sequence[selected_sequence[0]][index].duration
        if duration < h_box_total_min_size / 10:
            duration = h_box_total_min_size / 10
        if index < len(signal_sequence[selected_sequence[0]]) and i < len(signal_sequence[selected_sequence[0]][index].lights):
            get_label(i, index).setData([signal_sequence[selected_sequence[0]][index].lights[i] for _ in range(int(duration))])
        get_label(i, index).setMinimumSize(duration * 10, 25)
        get_label(i, index).setMaximumSize(duration * 10, 25)


def get_inner_h_box(index) -> QHBoxLayout:
    return duration_h_boxes[selected_sequence[0]][index]


def add_edits_to_h_box(index):
    remove_edits_from_h_box()
    h_box = get_inner_h_box(index)
    spacer_left: QSpacerItem = h_box.itemAt(0)
    spacer_right: QSpacerItem = h_box.itemAt(h_box.count() - 1)

    if selected_sequence[0] not in edit_buttons:
        edit_buttons[selected_sequence[0]] = []
    # add the edit buttons
    decrease_button = QPushButton("-")
    decrease_button.setStyleSheet(button_style_sheet)
    decrease_button.clicked.connect(lambda: decrease_duration_button(index))
    h_box.insertWidget(0, decrease_button)
    edit_buttons[selected_sequence[0]].append(decrease_button)

    increase_button = QPushButton("+")
    increase_button.setStyleSheet(button_style_sheet)
    increase_button.clicked.connect(lambda: increase_duration_button(index))
    h_box.addWidget(increase_button)
    edit_buttons[selected_sequence[0]].append(increase_button)

    # readjust the spacers for the buttons
    spacer_left.changeSize(spacer_left.sizeHint().width() - 52, 0, QSizePolicy.Minimum, QSizePolicy.Fixed)
    spacer_right.changeSize(spacer_right.sizeHint().width() - 52, 0, QSizePolicy.Minimum, QSizePolicy.Fixed)


def remove_edits_from_h_box():
    for i in range(len(duration_h_boxes[selected_sequence[0]])):
        if get_inner_h_box(i).count() > 3:
            h_box = get_inner_h_box(i)

            # Remove buttons from
            h_box.removeWidget(edit_buttons[selected_sequence[0]][0])
            h_box.removeWidget(edit_buttons[selected_sequence[0]][1])
            edit_buttons[selected_sequence[0]].pop(0)
            edit_buttons[selected_sequence[0]].pop(0)

            spacer_left: QSpacerItem = h_box.itemAt(0)
            spacer_right: QSpacerItem = h_box.itemAt(h_box.count() - 1)

            # readjust the spacers for the buttons
            spacer_left.changeSize(spacer_left.sizeHint().width() + 52, 0, QSizePolicy.Minimum, QSizePolicy.Fixed)
            spacer_right.changeSize(spacer_right.sizeHint().width() + 52, 0, QSizePolicy.Minimum, QSizePolicy.Fixed)


def refresh_h_box_spacer_sizes(index, size_change):
    h_box = get_inner_h_box(index)
    # 0 and last item are currently edit buttons
    spacer_left: QSpacerItem = h_box.itemAt(1)
    duration_label: QLabel = duration_labels[selected_sequence[0]][index]
    spacer_right: QSpacerItem = h_box.itemAt(h_box.count() - 2)

    # readjust the spacers for the buttons
    spacer_width = spacer_left.sizeHint().width() + size_change
    if int(duration_labels[selected_sequence[0]][index].text()) <= h_box_total_min_size / 10 - size_change / 5:
        spacer_width = min_duration_h_box_width
    spacer_left.changeSize(spacer_width, 0, QSizePolicy.Minimum, QSizePolicy.Fixed)
    spacer_right.changeSize(spacer_width, 0, QSizePolicy.Minimum, QSizePolicy.Fixed)

    # readjust duration label's text
    duration_label.setText(str(signal_sequence[selected_sequence[0]][index].duration))


def increase_duration_button(index):
    if signal_sequence[selected_sequence[0]][index].duration < 50:
        signal_sequence[selected_sequence[0]][index].duration += 1
    refresh_data_in_label(index)
    refresh_h_box_spacer_sizes(index, 5)


def decrease_duration_button(index):
    if signal_sequence[selected_sequence[0]][index].duration > 1:
        signal_sequence[selected_sequence[0]][index].duration -= 1
    refresh_data_in_label(index)
    refresh_h_box_spacer_sizes(index, -5)


def int_to_stylised_str(num):
    if num < 10:
        return "0" + str(num)
    return str(num)


class FLabelLayout(QHBoxLayout):

    def __init__(self, loop_id, page, scroll_area_widget):
        super(FLabelLayout, self).__init__()
        self.loop_id = loop_id
        self.loop_id_str = int_to_stylised_str(self.loop_id)
        self.page = page
        self.scroll_area_widget = scroll_area_widget
        self.draw_list = []
        self.setSpacing(0)
        self.init_labels()

    def create_flabel(self, id_str, x_size, style_sheet):
        label = FLabel(self.scroll_area_widget)
        label.label_id = self.loop_id_str + "_" + id_str
        label.label_pre_id = self.loop_id_str
        label.label_sub_id = id_str
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(label.sizePolicy().hasHeightForWidth())
        size_policy.setWidthForHeight(label.sizePolicy().hasWidthForHeight())
        label.setSizePolicy(size_policy)
        label.setMinimumSize(QSize(x_size, 25))
        label.setMaximumSize(QSize(x_size, 25))
        label.setFrameShape(QFrame.Box)
        label.setLineWidth(2)
        label.setText("")
        label.setStyleSheet(style_sheet)
        name = self.page + "_label_loopin_" + label.label_id
        label.setObjectName(name)
        return label

    def init_labels(self):
        # 0th row is for showing which line that represents, so it is fixed size 50 x 25
        label = self.create_flabel(int_to_stylised_str(0), 45, label_id_style_sheet)
        self.addWidget(label)

        for i in range(len(signal_sequence[selected_sequence[0]])):
            label = self.create_flabel(int_to_stylised_str(i + 1), signal_sequence[selected_sequence[0]][i].duration * 10, label_style_sheet)
            if i < len(signal_sequence[selected_sequence[0]]) and self.loop_id - 1 < len(signal_sequence[selected_sequence[0]][i].lights):
                label.clicked.connect(lambda x=i + 1: self.label_clicked(self.loop_id, x))
            insert_label(label, self.loop_id, i + 1)
            self.addWidget(label)

        refresh_data_in_all_labels()
        remove_edits_from_h_box()
        self.setAlignment(Qt.AlignLeft)

    def label_clicked(self, pre_id, sub_id):
        duration = signal_sequence[selected_sequence[0]][sub_id - 1].duration
        if duration < h_box_total_min_size / 10:
            duration = h_box_total_min_size / 10
        if edit_clicked[0] and \
                get_label(pre_id - 1, sub_id - 1).draw_list == [signal_sequence[selected_sequence[0]][sub_id - 1].lights[pre_id - 1]
                                                                for _ in range(int(duration))]:
            edit_clicked[0] = False
            refresh_data_in_all_labels()
            remove_edits_from_h_box()
        else:
            # Turn all the labels to their normal colors
            refresh_data_in_all_labels()
            for i in range(len(signal_sequence[selected_sequence[0]][0].lights)):
                for j in range(len(signal_sequence[selected_sequence[0]])):
                    if j != sub_id - 1:
                        temp_draw_list = get_label(i, j).draw_list
                        for k in range(len(temp_draw_list)):
                            temp_draw_list[k] = [x + 100 for x in temp_draw_list[k]]

                        get_label(i, j).setData(temp_draw_list)
                        #get_label(i, j).setData(
                           # [get_label(i, j).draw_list[k] + 100 for k in range(len(get_label(i, j).draw_list))])

            edit_clicked[0] = True
            add_edits_to_h_box(sub_id - 1)
