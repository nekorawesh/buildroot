import functools
import json
import os
import socket
# import fcntl
import struct

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from FHBoxLayout import FHBoxLayout, reset_arrays
from FLabelLayout import FLabelLayout, int_to_stylised_str, remove_edits_from_h_box, refresh_data_in_all_labels, \
    reset_labels
from hssMessages import *

from FLabel import FLabel, FLabel_Gprs
from Ui_untitled import Ui_MainWindow
from mqtt import SubThread, PubThread, MQTTPubTopics


phase_select_button_style_sheet = """
QPushButton {
    background-color: rgb(23, 87, 141);
    color: rgb(255, 255, 255);
    border-radius: 10px;
}
QPushButton:hover {
    background-color: rgb(29, 115, 185);
}
QPushButton:pressed {
    background-color: rgb(35, 135, 217);
    color: rgb(0, 0, 0);
}
"""


class deneme(QMainWindow):
    screen_backlight = 1

    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ### İlk açılış
        self.show_time("", False)
        self.fonk_errorRuntime("", False)
        self.fonk_PSMMeasurement("", False)
        self.fonk_moduleRuntime("", False)
        self.fonk_gateStateLog("", False)
        self.fonk_relayState("", False)
        self.fonk_userSettings("", False)
        self.ui.label_28.setText("")

        ### ekran akf kalma sayacı
        self.timerNormalTimeout = 120000
        self.screenSaverTimer = QTimer(self, interval=self.timerNormalTimeout, timeout=self.return_mainpage)
        self.screen_timer()
        self.screen_backlight = os.system("ls /sys/class/backlight")
        if self.screen_backlight == 0:
            self.screen_backlight = "5a000000.dsi.0"

        ###menü home toggle button
        # self.changeBtn()
        ###self.ui.btn_menu_home.clicked.connect(self.changeBtn) # simge toggle çalışmıyor

        ###menü erişimleri
        self.ui.btn_mn_item1.clicked.connect(self.btn_mn_item_clked)
        self.ui.btn_mn_item2.clicked.connect(self.btn_mn_item_clked)
        self.ui.btn_mn_item3.clicked.connect(self.btn_mn_item_clked)
        self.ui.btn_mn_item4.clicked.connect(self.btn_mn_item_clked)
        self.ui.btn_mn_item5.clicked.connect(self.btn_mn_item_clked)
        self.ui.btn_mn_item6.clicked.connect(self.btn_mn_item_clked)

        ###back button
        self.ui.btn_back.clicked.connect(self.back_fonk)

        ###save button
        self.ui.pushButton_3.clicked.connect(self.btn_save)

        ###keyboard
        self.ui.btn_num0.clicked.connect(self.loginKeyboard)
        self.ui.btn_num1.clicked.connect(self.loginKeyboard)
        self.ui.btn_num2.clicked.connect(self.loginKeyboard)
        self.ui.btn_num3.clicked.connect(self.loginKeyboard)
        self.ui.btn_num4.clicked.connect(self.loginKeyboard)
        self.ui.btn_num5.clicked.connect(self.loginKeyboard)
        self.ui.btn_num6.clicked.connect(self.loginKeyboard)
        self.ui.btn_num7.clicked.connect(self.loginKeyboard)
        self.ui.btn_num8.clicked.connect(self.loginKeyboard)
        self.ui.btn_num9.clicked.connect(self.loginKeyboard)
        self.ui.btn_numeraser.clicked.connect(self.loginKeyboard)
        ###login kısmı
        self.ui.btn_login.clicked.connect(self.loginKeyboard)

        ### ip Address
        self.ui.label_gprs = FLabel_Gprs(self.ui.frame_23)
        self.ui.label_gprs.setObjectName("label_gprs")
        self.ui.gridLayout_36.addWidget(self.ui.label_gprs, 0, 0, 1, 1)

        ###çeviri
        self.ui.trans = QTranslator(self)
        # self.change_func("en_US.qm")
        # lang_files = []
        for file in os.listdir("./lang"):
            if file.split(".")[-1] == "qm":
                self.lang_files.append("lang/" + file)

        self.which_lang()
        self.ui.btn_change_lang.clicked.connect(self.which_lang)

        ### Ayarlar Menüsü Erişimleri
        self.ui.btn_stgs_time_day.clicked.connect(self.btn_stgs_item_clked)
        self.ui.btn_stgs_lang.clicked.connect(self.btn_stgs_item_clked)
        self.ui.btn_stgs_gps.clicked.connect(self.btn_stgs_item_clked)
        self.ui.btn_stgs_connection.clicked.connect(self.btn_stgs_item_clked)
        self.ui.btn_stgs_lamb.clicked.connect(self.btn_stgs_item_clked)
        self.ui.btn_stgs_psm.clicked.connect(self.btn_stgs_item_clked)
        self.ui.btn_stgs_relay.clicked.connect(self.btn_stgs_item_clked)
        self.ui.btn_stgs_password.clicked.connect(self.btn_stgs_item_clked)
        self.ui.btn_stgs_configlock.clicked.connect(self.btn_stgs_item_clked)
        self.ui.btn_stgs_battery.clicked.connect(self.btn_stgs_item_clked)
        self.ui.btn_stgs_update.clicked.connect(self.btn_stgs_item_clked)
        self.ui.btn_stgs_factory.clicked.connect(self.btn_stgs_item_clked)
        ### ### Ayarlar/tarih saat ayarları
        self.ui.btn_num0_2.clicked.connect(self.dateChangeKeyboard)
        self.ui.btn_num1_2.clicked.connect(self.dateChangeKeyboard)
        self.ui.btn_num2_2.clicked.connect(self.dateChangeKeyboard)
        self.ui.btn_num3_2.clicked.connect(self.dateChangeKeyboard)
        self.ui.btn_num4_2.clicked.connect(self.dateChangeKeyboard)
        self.ui.btn_num5_2.clicked.connect(self.dateChangeKeyboard)
        self.ui.btn_num6_2.clicked.connect(self.dateChangeKeyboard)
        self.ui.btn_num7_2.clicked.connect(self.dateChangeKeyboard)
        self.ui.btn_num8_2.clicked.connect(self.dateChangeKeyboard)
        self.ui.btn_num9_2.clicked.connect(self.dateChangeKeyboard)
        self.ui.btn_numeraser_2.clicked.connect(self.dateChangeKeyboard)
        ### ### Ayarlar/bağlantı ayarları
        self.ui.radioButton.clicked.connect(self.show_connection_settings)
        self.ui.radioButton_2.clicked.connect(self.show_connection_settings)
        self.ui.radioButton_3.clicked.connect(self.show_connection_settings)
        self.ui.radioButton_4.clicked.connect(self.show_connection_settings)
        self.ui.radioButton_5.clicked.connect(self.show_connection_settings)
        ### ### Ayarlar/fabrika ayarları
        self.ui.pushButton_6.clicked.connect(
            lambda: self.sendMQTT(
                MQTTPubTopics.factoryReset.value, {
                    SharedValues.actionType.value: SharedValues.actionTypeSet.value,
                    SharedValues.values.value: {}
                }
            )
        )
        self.ui.pushButton_7.clicked.connect(self.back_fonk)
        ### ### Ayarlar/konfig kilidi
        self.ui.pushButton_14.clicked.connect(self.configbtn)
        self.ui.pushButton_16.clicked.connect(self.configbtn)
        ### ### Ayarlar/psm ayarları
        self.ui.pushButton.clicked.connect(self.changeOffsetPsm)
        self.ui.pushButton_2.clicked.connect(self.changeOffsetPsm)
        self.ui.pushButton_4.clicked.connect(self.changeOffsetPsm)
        self.ui.pushButton_5.clicked.connect(self.changeOffsetPsm)
        ### ### Ayarlar/şifre değişikliği
        self.load_users()
        self.ui.btn_num0_3.clicked.connect(self.keyboard_fonk3)
        self.ui.btn_num1_3.clicked.connect(self.keyboard_fonk3)
        self.ui.btn_num2_3.clicked.connect(self.keyboard_fonk3)
        self.ui.btn_num3_3.clicked.connect(self.keyboard_fonk3)
        self.ui.btn_num4_3.clicked.connect(self.keyboard_fonk3)
        self.ui.btn_num5_3.clicked.connect(self.keyboard_fonk3)
        self.ui.btn_num6_3.clicked.connect(self.keyboard_fonk3)
        self.ui.btn_num7_3.clicked.connect(self.keyboard_fonk3)
        self.ui.btn_num8_3.clicked.connect(self.keyboard_fonk3)
        self.ui.btn_num9_3.clicked.connect(self.keyboard_fonk3)
        self.ui.btn_numeraser_3.clicked.connect(self.keyboard_fonk3)
        ### ### Ayarlar/ekran parlaklık ayarı
        # self.ui.horizontalSlider.valueChanged.connect(lambda data: ###print(data))
        self.ui.horizontalSlider.sliderReleased.connect(self.screen_brightness)
        ### ### Ayarlar/harici pil
        self.ui.comboBox_4.currentIndexChanged.connect(self.battery)
        ### ### Ayarlar/Güncelleme
        self.ui.pushButton_13.clicked.connect(self.back_fonk)

        ###tarih saat timeri
        # timer1 = QTimer(self, interval=1000, timeout=self.showTime)
        # timer1.start()
        # self.showTime()

        # MQTT subscribe start
        self.startMqtt()

        ### log sayfası
        self.ui.listWidget_deviceslog.itemClicked.connect(self.log_selected)

        ### İncomes Menü Erişimleri
        self.ui.btn_incomes_loopreq.clicked.connect(self.btn_incomes_clked)
        self.ui.btn_incomes_looptra.clicked.connect(self.btn_incomes_clked)
        self.ui.btn_incomes_btnreq.clicked.connect(self.btn_incomes_clked)
        self.ui.btn_incomes_btntra.clicked.connect(self.btn_incomes_clked)

        ### Test Menü içerikleri
        self.ui.pushButton_10.clicked.connect(
            lambda: self.sendMQTT(
                MQTTPubTopics.relayState.value, {
                    SharedValues.actionType.value: SharedValues.actionTypeSet.value,
                    SharedValues.values.value: {
                        RelayState.isOn.value: True
                    }
                },
            )
        )
        self.ui.pushButton_11.clicked.connect(
            lambda: self.sendMQTT(
                MQTTPubTopics.relayState.value, {
                    SharedValues.actionType.value: SharedValues.actionTypeSet.value,
                    SharedValues.values.value: {
                        RelayState.isOn.value: False
                    }
                },
            )
        )

        self.sendMQTT(
            MQTTPubTopics.phaseCount.value, {
                SharedValues.actionType.value: SharedValues.actionTypeGet.value,
                SharedValues.values.value: {}
            }
        )

        self.page_signal_planer(
            "sigplan", "scrollAreaWidgetContents_3", "verticalLayout_16"
        )
        self.page_signal_planer(
            "buttontra", "scrollAreaWidgetContents_6", "verticalLayout_17"
        )
        self.page_signal_planer(
            "looptra", "scrollAreaWidgetContents_7", "verticalLayout_18"
        )

        ### Pre-load log messages
        self.last_log_index = ""
        self.wanted_log_index = ""
        self.sendMQTT(
            MQTTPubTopics.lastLogIndex.value, {
                SharedValues.actionType.value: SharedValues.actionTypeGet.value,
                SharedValues.values.value: {}
            }
        )

    def screen_brightness(self):
        os.system(
            "echo {} > /sys/class/backlight/{}/brightness".format(
                self.ui.horizontalSlider.value(), self.screen_backlight
            )
        )

    def battery(self):
        if not (self.user_settings == ""):
            ##print(self.ui.comboBox_4.currentIndex())
            self.btn_save_message = []
            self.btn_save_message.append(1)
            self.btn_save_message.append(MQTTPubTopics.userSettings.value)

            if self.ui.comboBox_4.currentIndex() == 0:
                self.user_settings[SharedValues.actionType.value] = SharedValues.actionTypeSet.value
                self.user_settings[SharedValues.values.value] = {UserSettings.isPowerOffSent.value: True}
                self.btn_save_message.append(self.user_settings)
            else:
                self.user_settings[SharedValues.actionType.value] = SharedValues.actionTypeSet.value
                self.user_settings[SharedValues.values.value] = {UserSettings.isPowerOffSent.value: False}
                self.btn_save_message.append(self.user_settings)
            ##print(self.user_settings)
            self.btn_save_mode(True)

    def configbtn(self):
        btn = self.sender()
        if btn.objectName() == "pushButton_14":
            self.user_settings[SharedValues.actionType.value] = SharedValues.actionTypeSet.value
            self.user_settings[SharedValues.values.value] = {UserSettings.isConfigOpen.value: True}
        else:
            self.user_settings[SharedValues.actionType.value] = SharedValues.actionTypeSet.value
            self.user_settings[SharedValues.values.value] = {UserSettings.isConfigOpen.value: False}
        self.sendMQTT(MQTTPubTopics.userSettings.value, self.user_settings)

    def page_signal_planer(self, page, scrollAreaWidget_id, verticalLayout_id):
        in_scrollAreaWidget = self.ui.content.findChild(QWidget, scrollAreaWidget_id)
        in_verticalLayout = self.ui.content.findChild(QVBoxLayout, verticalLayout_id)

        # add the duration on top of the lights on sigplan_edit
        if page.split("_")[0] == "sigplanEdit":
            hlayout = FHBoxLayout()
            in_verticalLayout.addLayout(hlayout)

        for loop_id in range(32):
            if page.split("_")[0] == "sigplanEdit":
                f_labels = FLabelLayout(loop_id + 1, page, in_scrollAreaWidget)
                in_verticalLayout.addLayout(f_labels)
                f_labels.setObjectName(page + "_label_loopin_" + int_to_stylised_str(loop_id + 1))

            else:
                if loop_id == 0:
                    continue
                self.ui.label_sig_plan = FLabel(in_scrollAreaWidget)
                self.ui.label_sig_plan.label_id = int_to_stylised_str(loop_id)
                self.ui.label_sig_plan.label_sub_id = "00"
                sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(
                    self.ui.label_sig_plan.sizePolicy().hasHeightForWidth()
                )
                sizePolicy.setWidthForHeight(
                    self.ui.label_sig_plan.sizePolicy().hasWidthForHeight()
                )
                self.ui.label_sig_plan.setSizePolicy(sizePolicy)
                # TODO set the size of the label according to the length of the program, so scroll bar on the bottom shows up
                self.ui.label_sig_plan.setMinimumSize(QSize(0, 25))
                self.ui.label_sig_plan.setMaximumSize(QSize(16777215, 25))
                self.ui.label_sig_plan.setFrameShape(QFrame.Box)
                self.ui.label_sig_plan.setLineWidth(2)
                self.ui.label_sig_plan.setText("")
                self.ui.label_sig_plan.setStyleSheet(
                    "color: rgb(23, 87, 141);\n"
                    "border-bottom: 2px solid;\n"
                    "border-bottom-color: rgb(23, 87, 141);\n"
                    "border-left: 2px solid;\n"
                    "border-left-color: rgb(23, 87, 141);\n"
                    "border-style: outset;"
                )
                # self.ui.label_sig_plan.setObjectName(name)
                name = page + "_label_loopin_" + int_to_stylised_str(loop_id)
                self.ui.label_sig_plan.setObjectName(name)
                in_verticalLayout.addWidget(self.ui.label_sig_plan)

    # self.ui.verticalLayout.addWidget(self.ui.scrollArea_5)

    def draw_sig_plan(
            self, page, scrool, data, mod
    ):  # signal buna bağlanacak dataları ekleyip refresh atacak #mod0 sig plan mod1 loopbtn
        scroll = self.ui.content.findChild(QScrollArea, scrool)
        for loopin in data:
            name = page + "_label_loopin_"
            if len(str(loopin["number"])) < 2:
                name = name + "0" + str(loopin["number"])
            else:
                name = name + str(loopin["number"])

            label_f = scroll.findChild(FLabel, name)
            if label_f is not None:
                if mod:
                    label_f.data_process(loopin["signal"])
                else:
                    if loopin["state"]:
                        label_f.data_process(4)
                    else:
                        label_f.data_process(1)

        """
		self.scrollArea = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
		self.widget = QWidget()  # Widget that contains the collection of Vertical Box
		self.gridbox = QGridLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

		self.gridbox.addWidget(QLabel("Phases"), 0, 0)
		self.gridbox.addWidget(QLabel("Transitions"), 0, 1)

		self.gridbox.addWidget(QPushButton("Phase 1"), 1, 0)
		self.gridbox.addWidget(QPushButton("Phase 2"), 2, 0)
		self.gridbox.addWidget(QPushButton("Phase 1 > 2"), 1, 1)

		self.widget.setLayout(self.gridbox)
		self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		# Enable one finger scrolling
		QScroller.grabGesture(self.scrollArea, QScroller.LeftMouseButtonGesture)
		self.scrollArea.setWidget(self.widget)

		scene.addWidget(self.scrollArea)

		#self.setCentralWidget(self.scrollArea)
		"""

    #############################################################

    lang_num_in_list = -1
    currentLang = ""
    lang_files = []
    phase_labels = []

    def which_lang(self):
        self.lang_num_in_list = self.lang_num_in_list + 1
        if self.lang_num_in_list >= len(self.lang_files):
            self.lang_num_in_list = self.lang_num_in_list - len(self.lang_files)
        self.change_func(self.lang_files[self.lang_num_in_list])
        if self.currentLang == Language.Turkish.value:
            self.currentLang = Language.English.value
            self.change_lang()
        # If english, or not defined
        else:
            self.currentLang = Language.Turkish.value
            self.change_lang()

    def change_lang(self):
        for i in range(len(self.phase_labels)):
            self.phase_labels[i].setText(phase_language[self.currentLang][i])

    # widget_history = []
    # def changeBtn(self):
    #     # if button is checked
    #     if self.ui.btn_menu_home.isChecked():

    #         # setting background color to light-blue
    #         #self.ui.btn_menu_home.setStyleSheet("background-color : lightblue")
    #         self.ui.lineEdit.clear()
    #         self.ui.lineEdit_2.clear()
    #         self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
    #         self.widget_history.append(self.ui.stackedWidget)
    #         self.page_position_for_label(self.ui.page_2.accessibleName())

    #     # if it is unchecked
    #     else:

    #         # set background color back to light-grey
    #         #self.ui.btn_menu_home.setStyleSheet("background-color : lightgrey")
    #         self.ui.stackedWidget.setCurrentWidget(self.ui.page)
    #         self.widget_history = []
    #         self.page_position_for_label(self.ui.page.accessibleName())

    active_user = 0

    def login_fonk(self, usr_name, usr_password):
        self.btn_save_mode(False)
        for user in self.accounts:
            if usr_name == user and usr_password == self.accounts[user]:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_menu)
                self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_menu_alt)
                self.ui.lineEdit.clear()
                self.ui.lineEdit_2.clear()
                self.page_position_for_label(self.ui.page_menu_alt.accessibleName())
                self.ui.label_8.setText(user)
                self.active_user = user
            else:
                self.ui.lineEdit.clear()
                self.ui.lineEdit_2.clear()

    widget_history = []

    def back_fonk(self):
        ##print(self.widget_history)
        # Restart the screensaver timer each time this button is pressed
        self.screenSaverTimer.stop()
        self.screenSaverTimer.start()
        self.btn_save_mode(False)
        if self.widget_history != []:
            if len(self.widget_history) == 1:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page)
                ###self.ui.btn_menu_home.setChecked(False)
                del self.widget_history[-1]
                self.page_position_for_label(self.ui.page.accessibleName())
                self.ui.btn_back.setText("Menü")
                self.active_user = 0
            elif len(self.widget_history) == 2:
                self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_menu_alt)
                self.ui.stackedWidget_5.setCurrentWidget(self.ui.page_4)
                del self.widget_history[-1]
                self.page_position_for_label(self.ui.page_menu_alt.accessibleName())
                self.sendMQTT(
                    MQTTPubTopics.startSignalGroupSignals.value, {
                        SharedValues.actionType.value: SharedValues.actionTypeSet.value,
                        SharedValues.values.value: {
                            StartSignalGroupSignals.start.value: False
                        }
                    }
                )
                self.sendMQTT(
                    MQTTPubTopics.startInputDemand.value, {
                        SharedValues.actionType.value: SharedValues.actionTypeSet.value,
                        SharedValues.values.value: {
                            StartInputDemand.start.value: False
                        }
                    },
                )
                FLabel.ekleSil()
            elif len(self.widget_history) == 3:
                if self.widget_history[2].objectName() == "stackedWidget_4":
                    self.ui.stackedWidget_4.setCurrentWidget(self.ui.page_incomes_main)
                    self.page_position_for_label(
                        self.ui.page_incomes_main.accessibleName()
                    )
                elif self.widget_history[2].objectName() == "stackedWidget_5":
                    self.ui.stackedWidget_5.setCurrentWidget(self.ui.page_4)
                    self.page_position_for_label(
                        self.ui.page_incomes_main.accessibleName()
                    )
                    remove_edits_from_h_box()
                else:
                    self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_settings_main)
                    self.page_position_for_label(
                        self.ui.page_settings_main.accessibleName()
                    )
                del self.widget_history[-1]

        else:
            ##print(self.widget_history)
            self.ui.btn_back.setText("Geri")
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear()
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_2)
            self.widget_history.append(self.ui.stackedWidget)
            self.page_position_for_label(self.ui.page_2.accessibleName())

    # self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_settings_main)
    # del self.widget_history[-1]
    # self.page_position_for_label(self.ui.page_settings_main.accessibleName())

    def return_mainpage(self):  ## back butonda ki ile aynı olmalı
        self.btn_save_mode(False)
        self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_menu_alt)
        self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_settings_main)
        self.ui.stackedWidget_4.setCurrentWidget(self.ui.page_incomes_main)
        self.ui.stackedWidget_5.setCurrentWidget(self.ui.page_4)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page)
        ###self.ui.btn_menu_home.setChecked(False)
        self.widget_history = []
        self.page_position_for_label(self.ui.page.accessibleName())
        self.ui.btn_back.setText("Menü")
        self.active_user = 0
        # TODO: uncomment these when working on the device itself
        # if not (self.screen_backlight == 1):
        #    os.system(
        #        "echo 15 > /sys/class/backlight/{}/bl_power".format(
        #            self.screen_backlight
        #        )
        #    )

    def btn_mn_item_clked(self):
        btn = self.sender()
        self.widget_history.append(self.ui.stackedWidget_2)
        self.btn_save_mode(False)

        if btn.objectName() == "btn_mn_item1":
            # TODO Find a better method for screensaver
            # Stop the screensaver timer in this page, it will get activated
            # again when back button is pressed
            self.screenSaverTimer.stop()
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_mn_item1)
            self.page_position_for_label(self.ui.page_mn_item1.accessibleName())
            self.sendMQTT(
                MQTTPubTopics.startSignalGroupSignals.value, {
                    SharedValues.actionType.value: SharedValues.actionTypeSet.value,
                    SharedValues.values.value: {
                        StartSignalGroupSignals.start.value: True
                    }
                },
            )

        elif btn.objectName() == "btn_mn_item2":
            # FIXME too many open files
            # Ask for logs again, in case there are new ones since last update
            self.last_log_index = ""
            self.wanted_log_index = ""
            self.sendMQTT(
                MQTTPubTopics.lastLogIndex.value, {
                    SharedValues.actionType.value: SharedValues.actionTypeGet.value,
                    SharedValues.values.value: {}
                }
            )
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_mn_item2)
            self.page_position_for_label(self.ui.page_mn_item2.accessibleName())

        elif btn.objectName() == "btn_mn_item3":
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_mn_item3)
            self.page_position_for_label(self.ui.page_mn_item3.accessibleName())

        elif btn.objectName() == "btn_mn_item4":
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_mn_item_sigplan_edit)
            self.page_position_for_label(self.ui.page_mn_item_sigplan_edit.accessibleName())

        elif btn.objectName() == "btn_mn_item5":
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_mn_item5)
            self.ui.stackedWidget_4.setCurrentWidget(self.ui.page_incomes_main)
            self.page_position_for_label(self.ui.page_mn_item5.accessibleName())

        elif btn.objectName() == "btn_mn_item6":
            self.ui.stackedWidget_2.setCurrentWidget(self.ui.page_mn_item6)
            self.page_position_for_label(self.ui.page_mn_item6.accessibleName())

    def loginKeyboard(self):
        # Restart the screensaver timer when pressed
        self.screenSaverTimer.stop()
        self.screenSaverTimer.start()
        btn = self.sender()
        # ##print(btn.objectName())
        if len(self.ui.lineEdit.text()) < 4:
            slcted_line = self.ui.lineEdit
        elif len(self.ui.lineEdit_2.text()) < 4:
            slcted_line = self.ui.lineEdit_2
        else:
            slcted_line = ""
        if slcted_line != "":
            if btn.objectName() == "btn_num0":
                slcted_line.setText(slcted_line.text() + "0")
            elif btn.objectName() == "btn_num1":
                slcted_line.setText(slcted_line.text() + "1")
            elif btn.objectName() == "btn_num2":
                slcted_line.setText(slcted_line.text() + "2")
            elif btn.objectName() == "btn_num3":
                slcted_line.setText(slcted_line.text() + "3")
            elif btn.objectName() == "btn_num4":
                slcted_line.setText(slcted_line.text() + "4")
            elif btn.objectName() == "btn_num5":
                slcted_line.setText(slcted_line.text() + "5")
            elif btn.objectName() == "btn_num6":
                slcted_line.setText(slcted_line.text() + "6")
            elif btn.objectName() == "btn_num7":
                slcted_line.setText(slcted_line.text() + "7")
            elif btn.objectName() == "btn_num8":
                slcted_line.setText(slcted_line.text() + "8")
            elif btn.objectName() == "btn_num9":
                slcted_line.setText(slcted_line.text() + "9")
            elif btn.objectName() == "btn_numeraser":
                if len(self.ui.lineEdit_2.text()) == 0:
                    slcted_line = self.ui.lineEdit
                slcted_line.setText(slcted_line.text()[:-1])
        else:
            if btn.objectName() == "btn_numeraser":
                self.ui.lineEdit_2.setText(self.ui.lineEdit_2.text()[:-1])
            elif btn.objectName() == "btn_login":
                usr_name = self.ui.lineEdit.text()
                usr_password = self.ui.lineEdit_2.text()
                self.login_fonk(usr_name, usr_password)

    def dateChangeKeyboard(self):
        btn = self.sender()
        selected_line = ""
        if len(self.ui.lineEdit_3.text()) < 2:
            selected_line = self.ui.lineEdit_3
        elif len(self.ui.lineEdit_4.text()) < 2:
            selected_line = self.ui.lineEdit_4
        elif len(self.ui.lineEdit_5.text()) < 2:
            selected_line = self.ui.lineEdit_5
        elif len(self.ui.lineEdit_6.text()) < 2:
            selected_line = self.ui.lineEdit_6
        elif len(self.ui.lineEdit_7.text()) < 4:
            selected_line = self.ui.lineEdit_7

        if selected_line != "":
            if btn.objectName() == "btn_num0_2":
                selected_line.setText(selected_line.text() + "0")
            elif btn.objectName() == "btn_num1_2":
                selected_line.setText(selected_line.text() + "1")
            elif btn.objectName() == "btn_num2_2":
                selected_line.setText(selected_line.text() + "2")
            elif btn.objectName() == "btn_num3_2":
                selected_line.setText(selected_line.text() + "3")
            elif btn.objectName() == "btn_num4_2":
                selected_line.setText(selected_line.text() + "4")
            elif btn.objectName() == "btn_num5_2":
                selected_line.setText(selected_line.text() + "5")
            elif btn.objectName() == "btn_num6_2":
                selected_line.setText(selected_line.text() + "6")
            elif btn.objectName() == "btn_num7_2":
                selected_line.setText(selected_line.text() + "7")
            elif btn.objectName() == "btn_num8_2":
                selected_line.setText(selected_line.text() + "8")
            elif btn.objectName() == "btn_num9_2":
                selected_line.setText(selected_line.text() + "9")
            elif btn.objectName() == "btn_numeraser_2":
                if len(self.ui.lineEdit_7.text()) == 0:
                    selected_line = self.ui.lineEdit_6
                if len(self.ui.lineEdit_6.text()) == 0:
                    selected_line = self.ui.lineEdit_5
                if len(self.ui.lineEdit_5.text()) == 0:
                    selected_line = self.ui.lineEdit_4
                if len(self.ui.lineEdit_4.text()) == 0:
                    selected_line = self.ui.lineEdit_3
                selected_line.setText(selected_line.text()[:-1])
        else:
            if btn.objectName() == "btn_numeraser_2":
                self.ui.lineEdit_7.setText(self.ui.lineEdit_7.text()[:-1])

        if (
                (len(self.ui.lineEdit_3.text()) == 2)
                and (len(self.ui.lineEdit_4.text()) == 2)
                and (len(self.ui.lineEdit_5.text()) == 2)
                and (len(self.ui.lineEdit_6.text()) == 2)
                and (len(self.ui.lineEdit_7.text()) == 4)
        ):
            self.btn_save_message = []
            self.btn_save_message.append(1)
            self.btn_save_message.append(MQTTPubTopics.time.value)
            self.btn_save_message.append(
                {
                    SharedValues.actionType.value: SharedValues.actionTypeSet.value,
                    SharedValues.values.value: {
                        TimeValues.source.value: 2,
                        TimeValues.isDST.value: self.ui.comboBox_3.currentIndex(),
                        TimeValues.second.value: 1,
                        TimeValues.minute.value: int(self.ui.lineEdit_4.text()),
                        TimeValues.hour.value: int(self.ui.lineEdit_3.text()),
                        TimeValues.day.value: int(self.ui.lineEdit_5.text()),
                        TimeValues.month.value: int(self.ui.lineEdit_6.text()),
                        TimeValues.year.value: int(self.ui.lineEdit_7.text()[-2:])
                    }
                }
            )

            self.btn_save_mode(True)
        else:
            self.btn_save_mode(False)

    def keyboard_fonk3(self):
        btn = self.sender()
        # ##print(btn.objectName())
        if len(self.ui.lineEdit_8.text()) < 4:
            slcted_line = self.ui.lineEdit_8
        elif len(self.ui.lineEdit_9.text()) < 4:
            slcted_line = self.ui.lineEdit_9
        else:
            slcted_line = ""
        if slcted_line != "":
            if btn.objectName() == "btn_num0_3":
                slcted_line.setText(slcted_line.text() + "0")
            elif btn.objectName() == "btn_num1_3":
                slcted_line.setText(slcted_line.text() + "1")
            elif btn.objectName() == "btn_num2_3":
                slcted_line.setText(slcted_line.text() + "2")
            elif btn.objectName() == "btn_num3_3":
                slcted_line.setText(slcted_line.text() + "3")
            elif btn.objectName() == "btn_num4_3":
                slcted_line.setText(slcted_line.text() + "4")
            elif btn.objectName() == "btn_num5_3":
                slcted_line.setText(slcted_line.text() + "5")
            elif btn.objectName() == "btn_num6_3":
                slcted_line.setText(slcted_line.text() + "6")
            elif btn.objectName() == "btn_num7_3":
                slcted_line.setText(slcted_line.text() + "7")
            elif btn.objectName() == "btn_num8_3":
                slcted_line.setText(slcted_line.text() + "8")
            elif btn.objectName() == "btn_num9_3":
                slcted_line.setText(slcted_line.text() + "9")
            elif btn.objectName() == "btn_numeraser_3":
                if len(self.ui.lineEdit_9.text()) == 0:
                    slcted_line = self.ui.lineEdit_8
                slcted_line.setText(slcted_line.text()[:-1])
        else:
            if btn.objectName() == "btn_numeraser_3":
                self.ui.lineEdit_9.setText(self.ui.lineEdit_9.text()[:-1])

        if (
                (len(self.ui.lineEdit_8.text()) == 4)
                and (len(self.ui.lineEdit_9.text()) == 4)
                and (self.ui.lineEdit_8.text() == self.ui.lineEdit_9.text())
        ):
            self.btn_save_message = []
            self.btn_save_message.append(0)
            self.btn_save_message.append(self.active_user)
            self.btn_save_message.append(self.ui.lineEdit_8.text())
            # ##print(self.btn_save_message)
            # ##print(self.ui.lineEdit_8.text())
            self.btn_save_mode(True)
        # self.btn_save() mqtt mesajı sıfırlama btn_savein içinde butonu aktif ve inaktif etme olacak
        # bi tane global değişken oluştur mqtt oraya atansın
        else:
            self.btn_save_mode(False)

    btn_save_message = []  # [mode,path,message] mode0 dosya, mode1 mqtt

    def btn_save_mode(self, AktiforInaktif):
        if AktiforInaktif and self.MQTT_server_error:
            self.ui.pushButton_3.setEnabled(True)
            self.ui.pushButton_3.setText("Save")
        else:
            self.ui.pushButton_3.setEnabled(False)
            self.ui.pushButton_3.setText("")

    def btn_save(self):
        ##print(self.btn_save_message)
        if not (len(self.btn_save_message) == 0):
            self.btn_save_mode(False)
            if self.btn_save_message[0] == 0:  # şifre değişikliği kaydet [mode,kullanıcıadi,şifre]
                ##print(self.btn_save_message)
                self.accounts[str(self.btn_save_message[1])] = str(
                    self.btn_save_message[2]
                )
                user_file = open("user.accounts", "w")
                user_file.writelines(str(self.accounts))
                user_file.close()

            if self.btn_save_message[0] == 1:  # mqtt mesajı yolla [mode,path,message]
                self.sendMQTT(self.btn_save_message[1], self.btn_save_message[2])

            self.back_fonk()

    def page_position_for_label(self, position):
        self.ui.label_position.setText(position)

    @pyqtSlot(int)
    def change_func(self, data):
        if data:
            self.ui.trans.load(data)
            QApplication.instance().installTranslator(self.ui.trans)
        else:
            QApplication.instance().removeTranslator(self.ui.trans)

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.ui.retranslateUi(self)
        super(deneme, self).changeEvent(event)

    def btn_stgs_item_clked(self):
        btn = self.sender()
        self.widget_history.append(self.ui.stackedWidget_3)
        self.btn_save_mode(False)
        if btn.objectName() == "btn_stgs_time_day":
            self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_stgs_time_day)
            self.page_position_for_label(self.ui.page_stgs_time_day.accessibleName())
            self.time_set = True
        elif btn.objectName() == "btn_stgs_lang":
            self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_stgs_lang)
            self.page_position_for_label(self.ui.page_stgs_lang.accessibleName())
        elif btn.objectName() == "btn_stgs_relay":
            self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_stgs_relay)
            self.page_position_for_label(self.ui.page_stgs_lang.accessibleName())
        elif btn.objectName() == "btn_stgs_gps":
            self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_stgs_gps)
            self.page_position_for_label(self.ui.page_stgs_gps.accessibleName())
        elif btn.objectName() == "btn_stgs_connection":
            self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_stgs_connection)
            self.page_position_for_label(self.ui.page_stgs_connection.accessibleName())
            self.connection_settings_set = True
        elif btn.objectName() == "btn_stgs_lamb":
            self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_stgs_lamb)
            self.page_position_for_label(self.ui.page_stgs_lamb.accessibleName())
        elif btn.objectName() == "btn_stgs_psm":
            self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_stgs_psm)
            self.page_position_for_label(self.ui.page_stgs_psm.accessibleName())
            self.sendMQTT(
                MQTTPubTopics.PSMMeasurement.value, {
                    SharedValues.actionType.value: SharedValues.actionTypeGet.value,
                    SharedValues.values.value: {}
                }
            )
        elif btn.objectName() == "btn_stgs_password":
            self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_stgs_password)
            self.page_position_for_label(self.ui.page_stgs_password.accessibleName())
            self.ui.lineEdit_8.setText("")
            self.ui.lineEdit_9.setText("")
        elif btn.objectName() == "btn_stgs_configlock":
            self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_stgs_configlock)
            self.page_position_for_label(self.ui.page_stgs_configlock.accessibleName())
            self.sendMQTT(
                MQTTPubTopics.userSettings.value, {
                    SharedValues.actionType.value: SharedValues.actionTypeGet.value,
                    SharedValues.values.value: {}
                }
            )
        elif btn.objectName() == "btn_stgs_battery":
            self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_stgs_battery)
            self.page_position_for_label(self.ui.page_stgs_battery.accessibleName())
            self.sendMQTT(
                MQTTPubTopics.userSettings.value, {
                    SharedValues.actionType.value: SharedValues.actionTypeGet.value,
                    SharedValues.values.value: {}
                }
            )
        elif btn.objectName() == "btn_stgs_update":
            self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_stgs_update)
            self.page_position_for_label(self.ui.page_stgs_update.accessibleName())
        elif btn.objectName() == "btn_stgs_factory":
            self.ui.stackedWidget_3.setCurrentWidget(self.ui.page_stgs_factory)
            self.page_position_for_label(self.ui.page_stgs_factory.accessibleName())

    def changeOffsetPsm(self):
        btn = self.sender()
        if btn.objectName() == "pushButton":
            self.ui.label_100.setText(str(int(self.ui.label_100.text()) - 1))
            self.ui.label_104.setText(
                str(int(self.ui.label_114.text()) + int(self.ui.label_100.text()))
            )
        elif btn.objectName() == "pushButton_2":
            self.ui.label_100.setText(str(int(self.ui.label_100.text()) + 1))
            self.ui.label_104.setText(
                str(int(self.ui.label_114.text()) + int(self.ui.label_100.text()))
            )
        elif btn.objectName() == "pushButton_4":
            self.ui.label_101.setText(str(int(self.ui.label_101.text()) - 1))
            self.ui.label_105.setText(
                str(int(self.ui.label_118.text()) + int(self.ui.label_101.text()))
            )
        elif btn.objectName() == "pushButton_5":
            self.ui.label_101.setText(str(int(self.ui.label_101.text()) + 1))
            self.ui.label_105.setText(
                str(int(self.ui.label_118.text()) + int(self.ui.label_101.text()))
            )

    def log_selected(self, data):
        self.screenSaverTimer.stop()
        self.screenSaverTimer.start()
        self.ui.label_deviceslog.setText(data.text().replace(" - ", "\n"))

    accounts = {}

    def load_users(self):
        user_file = open("user.accounts", "r")
        accounts = user_file.readlines()
        accounts = str(accounts[0]).replace("'", '"')
        ##print(type(accounts[0]))
        ##print(accounts)
        if type(accounts) == type({}):
            pass
        else:
            accounts = json.loads(accounts)
        self.accounts = accounts
        user_file.close()

    # @pyqtSlot()
    # def showTime(self):
    #     time = QTime.currentTime()
    #     day = QDate.currentDate()
    #     text_time = time.toString("HH:mm ss" if time.second() % 2 == 0 else "HH:mm:ss")
    #     text_day = day.toString()
    #     self.ui.label_tarih.setText(text_day)
    #     self.ui.label_saat.setText(text_time)

    def startMqtt(self):
        ##print("thread start ")
        self.thread_sub = SubThread(self)
        self.thread_sub.signal_time.connect(self.show_time)
        self.thread_sub.signal_operationRuntime.connect(self.fonk_operationRuntime)
        self.thread_sub.signal_PSMMeasurement.connect(self.fonk_PSMMeasurement)
        self.thread_sub.signal_moduleRuntime.connect(self.fonk_moduleRuntime)
        self.thread_sub.signal_errorRuntime.connect(self.fonk_errorRuntime)
        self.thread_sub.signal_inputDemands.connect(self.fonk_inputDemands)
        self.thread_sub.signal_signalGroupSignals.connect(self.fonk_signalGroupSignals)
        self.thread_sub.signal_relayState.connect(self.fonk_relayState)
        self.thread_sub.signal_logInfo.connect(self.fonk_logInfo)
        self.thread_sub.signal_userSettings.connect(self.fonk_userSettings)
        self.thread_sub.signal_lastLogIndex.connect(self.fonk_lastLogIndex)
        self.thread_sub.signal_gateStateLog.connect(self.fonk_gateStateLog)
        self.thread_sub.signal_MQTT_server_error.connect(self.fonk_MQTT_server_error)
        self.thread_sub.signal_State.connect(self.fonk_State)
        self.thread_sub.signal_phaseCount.connect(self.fonk_phase_count)
        self.thread_sub.signal_stepCount.connect(self.fonk_step_count)
        self.thread_sub.signal_stepInfo.connect(self.fonk_step_info)
        # self.thread_sub.signal_time.connect(self.show_time)
        self.thread_sub.start()

    def sendMQTT(self, topic, payload):
        sendThread = PubThread(self)
        sendThread.MQTT_TOPIC = topic
        sendThread.changed_values(payload)
        sendThread.start()

    time_set = False

    def show_time(self, time_data, status=True):
        if status:
            LG = lambda x: "0{}".format(x) if (len(str(x)) < 2) else "{}".format(x)
            self.ui.label_tarih.setText(
                "{}.{}.{}".format(
                    LG(time_data["values"]["day"]),
                    LG(time_data["values"]["month"]),
                    2000 + time_data["values"]["year"],
                )
            )
            self.ui.label_saat.setText(
                "{}:{}:{}".format(
                    LG(time_data["values"]["hour"]),
                    LG(time_data["values"]["minute"]),
                    LG(time_data["values"]["second"]),
                )
                if time_data["values"]["second"] % 2 == 0
                else "{}:{} {}".format(
                    LG(time_data["values"]["hour"]),
                    LG(time_data["values"]["minute"]),
                    LG(time_data["values"]["second"]),
                )
            )
            if self.time_set:
                self.time_set = False
                ##print("time refreshed!!!!!!!!!!")
                self.ui.lineEdit_3.setText(LG(str(time_data["values"]["hour"])))
                self.ui.lineEdit_4.setText(LG(str(time_data["values"]["minute"])))
                self.ui.lineEdit_5.setText(LG(str(time_data["values"]["day"])))
                self.ui.lineEdit_6.setText(LG(str(time_data["values"]["month"])))
                self.ui.lineEdit_7.setText(str(2000 + int(time_data["values"]["year"])))
        else:
            self.ui.label_tarih.setText("--.--.----")
            self.ui.label_saat.setText("--.--")
            self.ui.lineEdit_3.setText("--")
            self.ui.lineEdit_4.setText("--")
            self.ui.lineEdit_5.setText("--")
            self.ui.lineEdit_6.setText("--")
            self.ui.lineEdit_7.setText("--")

    connection_settings_set = False

    def show_connection_settings(self):
        btn = self.sender()
        data = {
            SharedValues.actionType.value: SharedValues.actionTypeSet.value,
            SharedValues.values.value: {
                GPRSSetting.modemType.value: 1,
                GPRSSetting.baudRate.value: GPRSSetting.baudRate9600.value
            }
        }
        if btn.objectName() == "radioButton":
            data[SharedValues.values.value][GPRSSetting.modemType.value] = 0
        elif btn.objectName() == "radioButton_2":
            data[SharedValues.values.value][GPRSSetting.modemType.value] = 1
        elif btn.objectName() == "radioButton_3":
            data[SharedValues.values.value][GPRSSetting.modemType.value] = 2
        elif btn.objectName() == "radioButton_4":
            data[SharedValues.values.value][GPRSSetting.modemType.value] = 3
        elif btn.objectName() == "radioButton_5":
            data[SharedValues.values.value][GPRSSetting.modemType.value] = 4
        self.sendMQTT(MQTTPubTopics.gprsSetting.value, data)
        connection_settings_set = True

    def fonk_operationRuntime(self, data):
        if not self.errorRuntime_error:
            state = data[SharedValues.values.value]["state"]
            # ##print(data)
            values = data[SharedValues.values.value]
            text_form = """
			<html><head>
			<style>p.small {line-height: 0.85;}</style>
			</head>
			<body>
			
			<p class="small">
			This is a paragraph<br>
			This is a paragrahp<br>
			</p>
			
			</body>
			</html>
			"""
            if state == 0:  # none
                self.ui.label_112.setText("run time")
                pass
            elif state == 1:  # any
                mtn = [
                    "-",
                    "DEVRE DIşI",
                    "FLAş",
                    "KAPALI",
                    "FAZ",
                    "FAZ DEğişimi",
                    "SEK",
                    "GÜVENLi GEÇiş",
                ]
                self.ui.label_112.setText(mtn[state])
            elif state == 2:  # no control
                pass
            elif state == 3:  # STATES_FLASH
                pass
            elif state == 4:  # closed
                pass
            elif state == 5:  # STATES_PHASE  phase
                mtn = "F{}:{}".format(values["arg1"], values["arg5"])
                mtn2 = "Min:{} Max:{}".format(values["arg3"], values["arg4"])
                self.ui.label_112.setText(mtn)
                self.ui.label.setText(mtn2)

            elif state == 6:  # STATES_SEQUENCE   sequence
                mtn = "S{}:{}".format(values["arg1"], values["arg7"])
                mtn2_lbl = "sek süre adim süre"
                mtn2 = "{}/{} {}/{} {}/{} {}/{}".format(
                    values["arg1"],
                    values["arg2"],
                    values["arg5"],
                    values["arg6"],
                    values["arg3"],
                    values["arg4"],
                    values["arg7"],
                    values["arg8"],
                )
                self.ui.label_112.setText(mtn)
                self.ui.label.setText(mtn2)
            elif state == 7:  # phase transition
                mtn = "F{}>{}".format(values["arg1"], values["arg2"])
                self.ui.label_112.setText(mtn)
            elif state == 8:  # secure transition
                pass
            elif state == 9:  # program loading
                mtn = [
                    "-",
                    "PROG.YÜK.BAşLADI",
                    "ANA->YEDEK BEL.",
                    "PROGRAM YÜKLENDı.",
                    "ANA->YEDEK BEL.HA",
                    "YEDEK->ANA BEL.",
                    "PROGRAM YÜKLENDı.",
                    "PROG.YEDEK->ANA H",
                    "PROGRAM YÜKLENıYOR..",
                    "PROGRAM YÜKLENDı.",
                    "PROGRAM YÜKLENEMEDı.",
                    "PROG.->ANA BEL.",
                    "PROG.->YEDEK BEL.",
                ]
                self.ui.label_112.setText(mtn[values["arg1"]])

    def fonk_PSMMeasurement(self, data, status=True):
        if status:
            text = ""
            key_list = []
            for key in data["values"].keys():
                key_list.append(key)
            ### ana ekran
            self.ui.label_29.setText(str(data["values"][key_list[0]]))
            # self.ui.label_30.setText(key_list[1]+":"+str(data["values"][key_list[1]]))
            # self.ui.label_31.setText(key_list[2]+":"+str(data["values"][key_list[2]]))
            # self.ui.label_32.setText(key_list[3]+":"+str(data["values"][key_list[3]]))
            ### ayarlar/psm ayarları
            self.ui.label_114.setText(str(data["values"]["psm1Voltage"]))
            self.ui.label_118.setText(str(data["values"]["psm2Voltage"]))
            self.ui.label_104.setText(
                str(data["values"]["psm1Voltage"] + int(self.ui.label_100.text()))
            )
            self.ui.label_105.setText(
                str(data["values"]["psm2Voltage"] + int(self.ui.label_101.text()))
            )
        else:
            self.ui.label_29.setText("--")

    # self.ui.label_118.setText("--")
    # self.ui.label_104.setText("--")
    # self.ui.label_105.setText("--")

    module_Runtime = ""

    def fonk_moduleRuntime(self, data, status=True):
        if status:
            ### Ana Ekran
            self.module_Runtime = data
            if not (data["values"]["gps"]["isModemConnected"]):
                self.ui.label_26.setStyleSheet(
                    "border: 4px solid;\nborder-radius: 10px;\nborder-style: outset;\ncolor: rgb(185, 0, 0);\nborder-color: rgb(185, 0, 0);"
                )
            else:
                self.ui.label_26.setStyleSheet(
                    "border: 4px solid;\nborder-radius: 10px;\nborder-style: outset;\ncolor: rgb(0, 255, 0);\nborder-color: rgb(0, 255, 0);"
                )

            if not (data["values"]["gprs"]["isModemConnected"]):
                self.ui.label_2.setStyleSheet(
                    "border: 4px solid;\nborder-radius: 10px;\nborder-style: outset;\ncolor: rgb(185, 0, 0);\nborder-color: rgb(185, 0, 0);"
                )
            else:
                self.ui.label_2.setStyleSheet(
                    "border: 4px solid;\n"
                    "border-radius: 10px;\n"
                    "border-style: outset;\n"
                    "color: rgb(0, 255, 0);\n"
                    "border-color: rgb(0, 255, 0);"
                )

            self.ui.label_gprs.data_process(
                (float(data["values"]["gprs"]["signalQuality"]) / 31) * 100
            )

            ### ana ekran
            self.ui.label_30.setText(str(data["values"]["lastInputs"]["digital"]))
            self.ui.label_31.setText(str(data["values"]["lastInputs"]["loop"]))

            ### bağlantı log
            gpsmodemType = ["none", "ublox", "telit"]
            gprsmodemType = ["ublox", "telit", "usr", "none", "quectel"]
            self.ui.label_113.setText(gpsmodemType[data["values"]["gps"]["modemType"]])
            self.ui.label_115.setText(data["values"]["gprs"]["imei"])
            self.ui.label_117.setText(data["values"]["ethernet"]["MAC"])
            self.ui.label_116.setText(data["values"]["gprs"]["operator"])
            # TODO: These only work in linux, uncomment them when working there
            """
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			ip_address = socket.inet_ntoa(fcntl.ioctl(
				s.fileno(),
				0x8915,  # SIOCGIFADDR
				struct.pack('256s', bytes('eth0'[:15], 'utf-8'))
			)[20:24])
			self.ui.label_123.setText(ip_address)
			"""
            self.ui.label_123.setText("192.168.10.120")
            ### ayarlar/gps ayarları
            self.ui.comboBox.setCurrentIndex(data["values"]["gps"]["modemType"])
            self.ui.comboBox_2.setCurrentIndex(data["values"]["gps"]["baudRate"])
            ### ayarlar/gprs ayarları

            if self.connection_settings_set:
                if data["values"]["gprs"]["modemType"] == 0:
                    self.ui.radioButton.setChecked(True)
                if data["values"]["gprs"]["modemType"] == 1:
                    self.ui.radioButton_2.setChecked(True)
                if data["values"]["gprs"]["modemType"] == 2:
                    self.ui.radioButton_3.setChecked(True)
                if data["values"]["gprs"]["modemType"] == 3:
                    self.ui.radioButton_4.setChecked(True)
                if data["values"]["gprs"]["modemType"] == 4:
                    self.ui.radioButton_5.setChecked(True)
                self.connection_settings_set = False
        else:
            self.ui.label_30.setText("--")
            self.ui.label_31.setText("--")
            self.ui.label_113.setText("--")
            self.ui.label_115.setText("--")
            self.ui.label_117.setText("--")
            self.ui.label_116.setText("--")

    errorRuntime_error = False

    def fonk_errorRuntime(self, data, status=True):
        if status:
            # ##print(data)
            data = data["values"]["errorRuntimes"][0]
            if data["signalingMode"] == 1:
                self.errorRuntime_error = False
            else:
                self.errorRuntime_error = True
                mtn = "Küme:{}".format(data["setNumber"])
                mtn2 = "{}".format(SignalingModesStr[self.currentLang][data["signalingMode"]])
                self.ui.label_112.setText(mtn)
                self.ui.label.setText(mtn2)
        else:
            self.ui.label_112.setText("MQTT Server Error")
            self.ui.label.setText("--")

    page = ""

    def fonk_inputDemands(self, data):
        for loopin in data["values"]["loopInputDemands"]:
            name = "loopreq_item"
            if len(str(loopin["number"])) < 2:
                name = name + "0" + str(loopin["number"])
            else:
                name = name + str(loopin["number"])

            buton = self.ui.frame_11.findChild(QPushButton, name)
            buton.setChecked(loopin["state"])

        for loopin in data["values"]["digitalInputDemands"]:
            name = "btnreq_item"
            if len(str(loopin["number"])) < 2:
                name = name + "0" + str(loopin["number"])
            else:
                name = name + str(loopin["number"])

            buton = self.ui.frame_12.findChild(QPushButton, name)
            buton.setChecked(loopin["state"])

        self.draw_sig_plan(
            "looptra", "scrollArea_7", data["values"]["loopInputDemands"], False
        )
        self.draw_sig_plan(
            "buttontra", "scrollArea_6", data["values"]["digitalInputDemands"], False
        )

    def fonk_signalGroupSignals(self, data):
        self.draw_sig_plan("sigplan", "scrollArea_5", data["values"]["sgSignals"], True)

    def fonk_relayState(self, data, status=True):
        if status:
            # ##print("relaystate" + str(data))
            if data["values"]["isOn"]:
                self.ui.label_17.setText(self.ui.pushButton_10.text())
            else:
                self.ui.label_17.setText(self.ui.pushButton_11.text())
        else:
            self.ui.label_17.setText("--")

    list_widget_item_count = 0
    log_messages = (
        {}
    )  #### loginfo ile index no gönderilir log indexler alınır listede alınan indexe atama yapılır log_messages={1:[log_message_short,log_message_long]}
    # logs variable keeps the logs. when log screen is called, ##print logs from this array
    logs = []

    def fonk_logInfo(self, data):  # lastlogindex ile karıştırmış olabilirim
        if not isinstance(self.last_log_index, type("")):
            LG = lambda x: "0{}".format(x) if (len(str(x)) < 2) else "{}".format(x)
            values = data[SharedValues.values.value]

            # " - " in this log message will be changed to newline when printed
            try:
                logMessage = " - !!!! UNKNOWN EVENT !!!! - log:" + str(values[EventParams.blog.value])
                if values[EventParams.blog.value] == Events.EVENT_SIGNAL_AT_SG.value or \
                        values[EventParams.blog.value] == Events.EVENT_INVALID_SIGNAL.value or \
                        values[EventParams.blog.value] == Events.EVENT_INVALID_SIGNAL_SEQUENCE.value:
                    logMessage = LogContents[self.currentLang][values[EventParams.blog.value]].format(
                        values[EventParams.bparam.value],
                        LogSignalTypes[self.currentLang][values[EventParams.sparam.value]],
                        LogSignalTypes[self.currentLang][values[EventParams.lparam.value]]
                    )

                elif values[EventParams.blog.value] == Events.EVENT_MODULE_MISSING.value or \
                        values[EventParams.blog.value] == Events.EVENT_MODULE_RESPONDS.value:
                    if values[EventParams.bparam.value] / 8 == 0:
                        logMessage = LogContents[self.currentLang][values[EventParams.blog.value]].format(
                            "SSM",
                            str(values[EventParams.bparam.value] + 1),
                            values[EventParams.lparam.value]
                        )
                    elif values[EventParams.bparam.value] / 8 == 2:
                        logMessage = LogContents[self.currentLang][values[EventParams.blog.value]].format(
                            "PSM",
                            str(values[EventParams.bparam.value] - 16),
                            values[EventParams.lparam.value]
                        )
                    elif values[EventParams.bparam.value] / 8 == 3:
                        logMessage = LogContents[self.currentLang][values[EventParams.blog.value]].format(
                            "IO",
                            str(values[EventParams.bparam.value] + 24),
                            values[EventParams.lparam.value]
                        )

                elif values[EventParams.blog.value] == Events.EVENT_VOLTAGE_VALUE_LOWER_BOUND.value or \
                        values[EventParams.blog.value] == Events.EVENT_VOLTAGE_VALUE_UPPER_BOUND.value:
                    logMessage = LogContents[self.currentLang][values[EventParams.blog.value]].format(
                        values[EventParams.sparam.value],
                        values[EventParams.lparam.value]
                    )

                elif values[EventParams.blog.value] == Events.EVENT_WORK_MODE_CHANGE.value:
                    logMessage = LogContents[self.currentLang][values[EventParams.blog.value]].format(
                        States[self.currentLang][values[EventParams.bparam.value] - 1],
                        States[self.currentLang][values[EventParams.sparam.value] - 1]
                    )

                elif values[EventParams.blog.value] == Events.EVENT_RESET_WINDOW_WATCHDOG.value or \
                        values[EventParams.blog.value] == Events.EVENT_RESET_INDEPENDENT_WATCHDOG.value or \
                        values[EventParams.blog.value] == Events.EVENT_RESET_LOW_POWER.value or \
                        values[EventParams.blog.value] == Events.EVENT_RESET_POWER_ON_CLEAR_CIRCUIT.value:
                    logMessage = LogContents[self.currentLang][values[EventParams.blog.value]].format(
                        Controller[values[EventParams.bparam.value]]
                    )

                elif values[EventParams.blog.value] == Events.EVENT_SET_SIGNALING_MODE_CHANGE.value:
                    if values[EventParams.sparam.value] == SignalingModes.SIGNALING_MODE_EMERGENCY_FLASH.value or \
                            values[EventParams.sparam.value] == SignalingModes.SIGNALING_MODE_EMERGENCY_FLASH_NEW.value:
                        values[EventParams.sparam.value] = 3
                    elif values[EventParams.sparam.value] == SignalingModes.SIGNALING_MODE_EMERGENCY_DARK.value:
                        values[EventParams.sparam.value] = 4

                    if values[EventParams.lparam.value] == SignalingModes.SIGNALING_MODE_EMERGENCY_FLASH.value or \
                            values[EventParams.sparam.value] == SignalingModes.SIGNALING_MODE_EMERGENCY_FLASH_NEW.value:
                        values[EventParams.sparam.value] = 3
                    elif values[EventParams.lparam.value] == SignalingModes.SIGNALING_MODE_EMERGENCY_DARK.value:
                        values[EventParams.lparam.value] = 4

                    logMessage = LogContents[self.currentLang][values[EventParams.blog.value]].format(
                        values[EventParams.bparam.value],
                        SignalingModesStr[self.currentLang][values[EventParams.sparam.value]],
                        SignalingModesStr[self.currentLang][values[EventParams.lparam.value]]
                    )

                elif values[EventParams.blog.value] == Events.EVENT_BATTERY_LOW.value or \
                        values[EventParams.blog.value] == Events.EVENT_BATTERY_NORMAL.value or \
                        values[EventParams.blog.value] == Events.EVENT_DOOR_OPEN.value or \
                        values[EventParams.blog.value] == Events.EVENT_DOOR_CLOSED.value or \
                        values[EventParams.blog.value] == Events.EVENT_VOLTAGE_VALUE_NORMAL.value or \
                        values[EventParams.blog.value] == Events.EVENT_FREQUENCY_VALUE_LOWER_BOUND.value or \
                        values[EventParams.blog.value] == Events.EVENT_FREQUENCY_VALUE_UPPER_BOUND.value or \
                        values[EventParams.blog.value] == Events.EVENT_FREQUENCY_VALUE_NORMAL.value or \
                        values[EventParams.blog.value] == Events.EVENT_USER_REQ_LCD_LOG_IN.value or \
                        values[EventParams.blog.value] == Events.EVENT_USER_REQ_LCD_LOG_OUT.value or \
                        values[EventParams.blog.value] == Events.EVENT_USER_REQ_LCD_LOG_IN_USERNAME_ERR.value or \
                        values[EventParams.blog.value] == Events.EVENT_USER_REQ_LCD_LOG_IN_PASSWORD_ERR.value:
                    logMessage = LogContents[self.currentLang][values[EventParams.blog.value]].format(
                        values[EventParams.sparam.value],
                        values[EventParams.lparam.value]
                    )

                elif values[EventParams.blog.value] == Events.EVENT_YELLOW_YELLOW_CONFLICT.value or \
                        values[EventParams.blog.value] == Events.EVENT_YELLOW_GREEN_CONFLICT.value or \
                        values[EventParams.blog.value] == Events.EVENT_GREEN_GREEN_CONFLICT.value:
                    logMessage = LogContents[self.currentLang][values[EventParams.blog.value]].format(
                        values[EventParams.bparam.value],
                        values[EventParams.sparam.value],
                        values[EventParams.lparam.value]
                    )

                else:
                    logMessage = LogContents[self.currentLang][values[EventParams.blog.value]].format(
                        values[EventParams.bparam.value],
                        values[EventParams.sparam.value],
                        values[EventParams.lparam.value]
                    )

            # For now, I have only encountered IndexError from bad log messages
            except Exception as e:
                logMessage = "There was a problem. - " + str(e) + \
                             " - Event: " + str(values[EventParams.blog.value]) + \
                             " - bparam: " + str(values[EventParams.bparam.value]) + \
                             " - sparam: " + str(values[EventParams.sparam.value]) + \
                             " - lparam: " + str(values[EventParams.lparam.value])

            log_message_short = "{}/{}/{} {}:{}:{} - {}".format(
                LG(values[EventParams.day.value]),
                LG(values[EventParams.month.value]),
                LG(values[EventParams.year.value]),
                LG(values[EventParams.hour.value]),
                LG(values[EventParams.minute.value]),
                LG(values[EventParams.second.value]),
                logMessage,
            )

            # If message isn't already in the array, add it
            if log_message_short not in self.logs:
                self.logs.append(log_message_short)
                self.list_widget_item_count = self.list_widget_item_count + 1
                self.ui.listWidget_deviceslog.insertItem(
                    self.list_widget_item_count, log_message_short
                )

            if isinstance(self.wanted_log_index, type("")):
                self.wanted_log_index = self.last_log_index - 1
                self.sendMQTT(
                    MQTTPubTopics.logInfo.value, {
                        SharedValues.actionType.value: SharedValues.actionTypeGet.value,
                        SharedValues.values.value: {
                            LogInfo.index.value: self.wanted_log_index
                        }
                    }
                )
            elif (self.last_log_index - self.wanted_log_index) < 20:
                self.wanted_log_index = self.wanted_log_index - 1
                self.sendMQTT(
                    MQTTPubTopics.logInfo.value, {
                        SharedValues.actionType.value: SharedValues.actionTypeGet.value,
                        SharedValues.values.value: {
                            LogInfo.index.value: self.wanted_log_index
                        }
                    }
                )
            elif (self.last_log_index - self.wanted_log_index) > 20:
                self.wanted_log_index = ""
                self.list_widget_item_count = 0

    last_log_index = ""
    wanted_log_index = ""

    def fonk_lastLogIndex(self, data):
        self.last_log_index = data["values"]["index"]
        self.sendMQTT(
            MQTTPubTopics.logInfo.value, {
                SharedValues.actionType.value: SharedValues.actionTypeGet.value,
                SharedValues.values.value: {
                    LogInfo.index.value: self.last_log_index
                }
            }
        )

    def fonk_gateStateLog(self, data, status=True):
        if status:
            data = data["values"]
            self.ui.label_32.setText(
                "{}/{}/{} {}:{}:{}".format(
                    data["day"],
                    data["month"],
                    data["year"],
                    data["hour"],
                    data["minute"],
                    data["second"],
                )
            )
        else:
            self.ui.label_32.setText("--")

    user_settings = {}

    def fonk_userSettings(self, data, status=True):
        if status:
            ##print(data)
            self.user_settings = data
            if data["values"]["isConfigOpen"] == True:
                self.ui.label_19.setText(self.ui.pushButton_14.text())
            else:
                self.ui.label_19.setText(self.ui.pushButton_16.text())
        else:
            self.ui.label_19.setText("--")

    MQTT_server_error = True

    def fonk_MQTT_server_error(self, status):
        if status:
            self.show_time("", False)
            self.fonk_errorRuntime("", False)
            self.fonk_PSMMeasurement("", False)
            self.fonk_moduleRuntime("", False)
            self.fonk_gateStateLog("", False)
            self.fonk_relayState("", False)
            self.fonk_userSettings("", False)
            self.ui.label_28.setText("")
            self.user_settings = {}
            self.MQTT_server_error = False
        else:
            self.MQTT_server_error = True

    def fonk_State(self, data):
        if data["values"]["state"]:
            self.screen_timer(True)

    last_sent_phase_index = 1

    def fonk_phase_count(self, data):
        self.last_sent_phase_index = 1
        seq_length[0] = int(data["values"]["phase"])
        self.send_step_count()

    def send_step_count(self):
        if self.last_sent_phase_index <= seq_length[0]:
            self.sendMQTT(
                MQTTPubTopics.stepCount.value, {
                    SharedValues.actionType.value: SharedValues.actionTypeGet.value,
                    SharedValues.values.value: {
                        StepCount.phase.value: str(self.last_sent_phase_index)
                    }
                }
            )
        else:
            # add the phase select buttons to sigplan_edit screen
            phase_buttons_layout = self.ui.content.findChild(QGridLayout, "gridLayout_40")
            phase_label = QLabel(phase_language[self.currentLang][0])
            phase_label.setAlignment(Qt.AlignCenter)
            phase_transition_label = QLabel(phase_language[self.currentLang][1])
            phase_transition_label.setAlignment(Qt.AlignCenter)
            phase_buttons_layout.addWidget(phase_label, 0, 0)
            phase_buttons_layout.addWidget(phase_transition_label, 0, 1)
            self.phase_labels.append(phase_label)
            self.phase_labels.append(phase_transition_label)

            phase_button_grid = 1
            phase_transition_button_grid = 1
            for i in range(len(signal_sequence)):
                button = QPushButton()
                button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
                button.setStyleSheet(phase_select_button_style_sheet)
                button.clicked.connect(
                    lambda ignore, x=i: self.edit_sigplan_buttons_pressed(list(signal_sequence.keys())[x]))
                # Transition phases have _ between the transition phase numbers
                button.setText("Phase " + list(signal_sequence.keys())[i])
                if len(list(signal_sequence.keys())[i].split("->")) == 2:
                    phase_buttons_layout.addWidget(button, phase_transition_button_grid, 1)
                    phase_transition_button_grid += 1
                else:
                    phase_buttons_layout.addWidget(button, phase_button_grid, 0)
                    phase_button_grid += 1

            ### Scrollarea atamaları incomes ve signal plan sayfaları için
            # self.ui.verticalLayout_16 = QVBoxLayout(self.ui.scrollAreaWidgetContents_3) #fonksiyon oluştur ve scrollAreaWidgetContents nesne halinde argüman olarak ver
            # self.ui.verticalLayout_16.setObjectName("verticalLayout_16")

            for seq in list(signal_sequence.keys()):
                page = QWidget()
                page.setObjectName("phase_page_" + seq)
                scroll_area = QScrollArea(page)
                scroll_area.setGeometry(QtCore.QRect(0, 0, 790, 279))
                scroll_area.setStyleSheet(scroll_bar_stylesheet)
                scroll_area.setFrameShape(QFrame.NoFrame)
                scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
                scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
                scroll_area.setWidgetResizable(True)
                scroll_area.setObjectName("phase_scrollArea_" + seq)
                scroll_area_contents = QWidget()
                scroll_area_contents.setGeometry(QtCore.QRect(0, 0, 776, 265))
                scroll_area_contents.setObjectName("phase_scroll_area_contents_" + seq)
                scroll_area_layout = QVBoxLayout(scroll_area_contents)
                scroll_area_layout.setContentsMargins(0, 0, 0, 0)
                scroll_area_layout.setSpacing(2)
                scroll_area_layout.setObjectName("phase_scroll_area_layout_" + seq)
                scroll_area.setWidget(scroll_area_contents)
                self.ui.stackedWidget_5.addWidget(page)

                selected_sequence[0] = seq
                self.page_signal_planer(
                    "sigplanEdit_" + "seq", scroll_area_contents.objectName(), scroll_area_layout.objectName()
                )

            selected_sequence[0] = ""


    last_sent_step_index = 1

    def fonk_step_count(self, data):
        self.last_sent_step_index = 1
        seq_count[self.last_sent_phase_index] = int(data[SharedValues.values.value][StepInfo.steps.value])
        self.get_each_steps()

    def get_each_steps(self):
        if self.last_sent_step_index <= seq_count[self.last_sent_phase_index]:
            self.sendMQTT(
                MQTTPubTopics.stepInfo.value, {
                    SharedValues.actionType.value: SharedValues.actionTypeGet.value,
                    SharedValues.values.value: {
                        StepInfo.phase.value: str(self.last_sent_phase_index),
                        StepInfo.steps.value: str(self.last_sent_step_index)
                    }
                }
            )
        else:
            self.last_sent_phase_index += 1
            self.send_step_count()

    def fonk_step_info(self, data):
        print(data[SharedValues.values.value][StepInfo.steps.value])
        if str(self.last_sent_phase_index) not in list(signal_sequence.keys()):
            signal_sequence[str(self.last_sent_phase_index)] = []

        data = [int(i) for i in data[SharedValues.values.value][StepInfo.steps.value].split(",")]
        light_array = [0 for _ in range(32)]
        # [0] is phase number, [1] is step number, [2] is duration
        # [-2] is last light's index, [-1] the last light
        for i in range(data[-2]):
            light_array[data[i*2 + 3] - 1] = data[2*i + 4]
        signal_sequence[str(self.last_sent_phase_index)].append(SignalSequence(light_array, data[2]))
        self.last_sent_step_index += 1
        self.get_each_steps()

    def btn_incomes_clked(self):
        # TODO Find a better method for screensaver
        # Stop the screensaver timer in this page, it will get activated
        # again when back button is pressed
        self.screenSaverTimer.stop()
        btn = self.sender()
        self.widget_history.append(
            self.ui.stackedWidget_4
        )  ######## geri butonu için ama çalışmıyor
        if btn.objectName() == "btn_incomes_loopreq":
            self.ui.stackedWidget_4.setCurrentWidget(self.ui.page_incomes_loopreq)
            self.page_position_for_label(self.ui.page_incomes_loopreq.accessibleName())
            self.sendMQTT(
                MQTTPubTopics.startInputDemands.value, {
                    SharedValues.actionType.value: SharedValues.actionTypeSet.value,
                    SharedValues.values.value: {
                        StartInputDemands.start.value: True
                    }
                }
            )
        ##print("btn_incomes_loopreq")
        elif btn.objectName() == "btn_incomes_looptra":
            self.ui.stackedWidget_4.setCurrentWidget(self.ui.page_incomes_looptra)
            self.page_position_for_label(self.ui.page_incomes_looptra.accessibleName())
            self.sendMQTT(
                MQTTPubTopics.startInputDemands.value, {
                    SharedValues.actionType.value: SharedValues.actionTypeSet.value,
                    SharedValues.values.value: {
                        StartInputDemands.start.value: True
                    }
                }
            )
        ##print("btn_incomes_looptra")
        elif btn.objectName() == "btn_incomes_btnreq":
            self.ui.stackedWidget_4.setCurrentWidget(self.ui.page_incomes_btnreq)
            self.page_position_for_label(self.ui.page_incomes_btnreq.accessibleName())
            self.sendMQTT(
                MQTTPubTopics.startInputDemands.value, {
                    SharedValues.actionType.value: SharedValues.actionTypeSet.value,
                    SharedValues.values.value: {
                        StartInputDemands.start.value: True
                    }
                }
            )
        ##print("btn_incomes_btnreq")
        ##print(self.ui.stackedWidget_4.currentIndex())
        elif btn.objectName() == "btn_incomes_btntra":
            self.ui.stackedWidget_4.setCurrentWidget(self.ui.page_incomes_btntra)
            self.page_position_for_label(self.ui.page_incomes_btntra.accessibleName())
            self.sendMQTT(
                MQTTPubTopics.startInputDemands.value, {
                    SharedValues.actionType.value: SharedValues.actionTypeSet.value,
                    SharedValues.values.value: {
                        StartInputDemands.start.value: True
                    }
                }
            )

    def edit_sigplan_buttons_pressed(self, button):
        self.screenSaverTimer.stop()
        self.widget_history.append(
            self.ui.stackedWidget_5
        )
        selected_sequence[0] = button
        refresh_data_in_all_labels()
        self.ui.stackedWidget_5.setCurrentWidget(
            self.ui.content.findChild(QWidget, "phase_page_" + button)
        )

    def get_from_ui(self, content_type, name):
        return self.ui.content.findChild(content_type, name)

    ##print("btn_incomes_btntra")
    ##print(self.ui.stackedWidget_4.currentIndex())
    ##print(self.ui.stackedWidget_4.parentWidget().objectName())

    def screen_timer(self, touched=False):
        # ##print("SCREEN AFK TIME RESETTED")
        self.screenSaverTimer.stop()
        self.screenSaverTimer.start()
        # TODO: uncomment these when working on the device itself
        # if (self.screen_backlight != 1) and touched:
        #   os.system(
        #       "echo 0 > /sys/class/backlight/{}/bl_power".format(
        #           self.screen_backlight
        #        )
        #    )  # max 255

    def eventFilter(self, obj, event):
        if event.type() in [QEvent.MouseButtonPress, QEvent.KeyPress]:
            self.screen_timer(True)
            return True

        return super(deneme, self).eventFilter(obj, event)


"""
uygulama = QApplication([])
window = deneme()
window.installEventFilter(window)
# window.showFullScreen()
window.show()
uygulama.exec_()
"""

uygulama = QApplication([])
scene = QGraphicsScene()
view = QGraphicsView()
proxy = QGraphicsProxyWidget()
window = deneme()
window.installEventFilter(window)
proxy = scene.addWidget(window)
view.setScene(scene)
view.rotate(90)
view.showFullScreen()
view.show()
uygulama.exec_()
