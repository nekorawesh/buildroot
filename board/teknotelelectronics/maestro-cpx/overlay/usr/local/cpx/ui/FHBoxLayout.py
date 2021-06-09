from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt

from hssMessages import duration_label_width, button_width, min_duration_h_box_width, signal_sequence, \
    selected_sequence

duration_label_style_sheet = """
QLabel {
    max-width: """ + str(duration_label_width) + """px;
    min-width: """ + str(duration_label_width) + """px;
}
"""

# Each h_box has [spacer][label][spacer]
# when edit buttons are added, it becomes: [button][spacer][label][spacer][button]
duration_h_boxes = {}
duration_labels = {}
edit_buttons = {}


def reset_arrays():
    for i in range(len(duration_h_boxes)):
        duration_h_boxes.pop(0)
    # clear labels before erasing them
    for i in range(len(duration_labels)):
        duration_labels.pop(0).deleteLater()
    for i in range(len(edit_buttons)):
        edit_buttons.pop(0)


class FHBoxLayout(QHBoxLayout):

    def __init__(self):
        super(FHBoxLayout, self).__init__()

        self.setSpacing(0)
        spacer = QSpacerItem(45, 0, QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.addSpacerItem(spacer)

        duration_h_boxes[selected_sequence[0]] = []
        duration_labels[selected_sequence[0]] = []

        for i in range(len(signal_sequence[selected_sequence[0]])):
            inner_hbox = QHBoxLayout()
            spacer_width = (signal_sequence[selected_sequence[0]][i].duration * 10 - 20) / 2
            if spacer_width < button_width + min_duration_h_box_width:
                spacer_width = button_width + min_duration_h_box_width

            spacer = QSpacerItem(spacer_width, 0, QSizePolicy.Minimum, QSizePolicy.Fixed)
            inner_hbox.addSpacerItem(spacer)

            label = QLabel(str(signal_sequence[selected_sequence[0]][i].duration))
            label.setStyleSheet(duration_label_style_sheet)
            label.setAlignment(Qt.AlignCenter)
            inner_hbox.addWidget(label)

            spacer = QSpacerItem(spacer_width, 0, QSizePolicy.Minimum, QSizePolicy.Fixed)
            inner_hbox.addSpacerItem(spacer)

            inner_hbox.setAlignment(Qt.AlignLeft)
            duration_h_boxes[selected_sequence[0]].append(inner_hbox)
            duration_labels[selected_sequence[0]].append(label)

            self.addLayout(inner_hbox)
            if i == len(signal_sequence[selected_sequence[0]]) - 1:
                spacer = QSpacerItem(150, 0, QSizePolicy.Expanding, QSizePolicy.Fixed)
                self.addSpacerItem(spacer)

        self.setAlignment(Qt.AlignLeft)

