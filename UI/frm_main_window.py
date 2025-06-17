# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDateEdit, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QStatusBar, QTextEdit,
    QTimeEdit, QToolBox, QVBoxLayout, QWidget)

class Ui_frm_main_window(object):
    def setupUi(self, frm_main_window):
        if not frm_main_window.objectName():
            frm_main_window.setObjectName(u"frm_main_window")
        frm_main_window.resize(644, 419)
        font = QFont()
        font.setFamilies([u"Calibri"])
        font.setPointSize(12)
        frm_main_window.setFont(font)
        self.centralwidget = QWidget(frm_main_window)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.wg_main_tasks = QWidget(self.centralwidget)
        self.wg_main_tasks.setObjectName(u"wg_main_tasks")
        self.verticalLayout_5 = QVBoxLayout(self.wg_main_tasks)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.lb_tasks = QLabel(self.wg_main_tasks)
        self.lb_tasks.setObjectName(u"lb_tasks")
        font1 = QFont()
        font1.setFamilies([u"Calibri"])
        font1.setPointSize(14)
        font1.setBold(True)
        self.lb_tasks.setFont(font1)
        self.lb_tasks.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_5.addWidget(self.lb_tasks)

        self.tb_tasks = QToolBox(self.wg_main_tasks)
        self.tb_tasks.setObjectName(u"tb_tasks")
        self.high = QWidget()
        self.high.setObjectName(u"high")
        self.high.setGeometry(QRect(0, 0, 274, 173))
        self.verticalLayout = QVBoxLayout(self.high)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lw_high = QListWidget(self.high)
        self.lw_high.setObjectName(u"lw_high")

        self.verticalLayout.addWidget(self.lw_high)

        self.tb_tasks.addItem(self.high, u"Hoch")
        self.medium = QWidget()
        self.medium.setObjectName(u"medium")
        self.medium.setGeometry(QRect(0, 0, 98, 91))
        self.verticalLayout_2 = QVBoxLayout(self.medium)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lw_medium = QListWidget(self.medium)
        self.lw_medium.setObjectName(u"lw_medium")

        self.verticalLayout_2.addWidget(self.lw_medium)

        self.tb_tasks.addItem(self.medium, u"Mittel")
        self.low = QWidget()
        self.low.setObjectName(u"low")
        self.low.setGeometry(QRect(0, 0, 98, 91))
        self.verticalLayout_3 = QVBoxLayout(self.low)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.lw_low = QListWidget(self.low)
        self.lw_low.setObjectName(u"lw_low")

        self.verticalLayout_3.addWidget(self.lw_low)

        self.tb_tasks.addItem(self.low, u"Niedrig")

        self.verticalLayout_5.addWidget(self.tb_tasks)

        self.wg_tasks_buttons = QWidget(self.wg_main_tasks)
        self.wg_tasks_buttons.setObjectName(u"wg_tasks_buttons")
        self.horizontalLayout = QHBoxLayout(self.wg_tasks_buttons)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pb_new_task = QPushButton(self.wg_tasks_buttons)
        self.pb_new_task.setObjectName(u"pb_new_task")
        self.pb_new_task.setMinimumSize(QSize(110, 30))
        self.pb_new_task.setMaximumSize(QSize(140, 40))

        self.horizontalLayout.addWidget(self.pb_new_task)

        self.pb_show_description = QPushButton(self.wg_tasks_buttons)
        self.pb_show_description.setObjectName(u"pb_show_description")
        self.pb_show_description.setMinimumSize(QSize(110, 30))
        self.pb_show_description.setMaximumSize(QSize(140, 40))
        self.pb_show_description.setCheckable(True)
        self.pb_show_description.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.pb_show_description)


        self.verticalLayout_5.addWidget(self.wg_tasks_buttons)


        self.horizontalLayout_3.addWidget(self.wg_main_tasks)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.wg_main_descripton = QWidget(self.centralwidget)
        self.wg_main_descripton.setObjectName(u"wg_main_descripton")
        self.verticalLayout_4 = QVBoxLayout(self.wg_main_descripton)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.lb_task_title = QLabel(self.wg_main_descripton)
        self.lb_task_title.setObjectName(u"lb_task_title")
        self.lb_task_title.setFont(font1)
        self.lb_task_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.lb_task_title)

        self.te_description = QTextEdit(self.wg_main_descripton)
        self.te_description.setObjectName(u"te_description")

        self.verticalLayout_4.addWidget(self.te_description)

        self.wg_description_time = QWidget(self.wg_main_descripton)
        self.wg_description_time.setObjectName(u"wg_description_time")
        self.wg_description_time.setFont(font)
        self.horizontalLayout_4 = QHBoxLayout(self.wg_description_time)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.ded_description = QDateEdit(self.wg_description_time)
        self.ded_description.setObjectName(u"ded_description")
        self.ded_description.setCalendarPopup(True)

        self.horizontalLayout_4.addWidget(self.ded_description)

        self.ted_description = QTimeEdit(self.wg_description_time)
        self.ted_description.setObjectName(u"ted_description")

        self.horizontalLayout_4.addWidget(self.ted_description)


        self.verticalLayout_4.addWidget(self.wg_description_time)

        self.wg_description_buttons = QWidget(self.wg_main_descripton)
        self.wg_description_buttons.setObjectName(u"wg_description_buttons")
        self.horizontalLayout_2 = QHBoxLayout(self.wg_description_buttons)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.pb_finish_task = QPushButton(self.wg_description_buttons)
        self.pb_finish_task.setObjectName(u"pb_finish_task")
        self.pb_finish_task.setMinimumSize(QSize(110, 30))
        self.pb_finish_task.setMaximumSize(QSize(140, 40))

        self.horizontalLayout_2.addWidget(self.pb_finish_task)

        self.pb_edit_task = QPushButton(self.wg_description_buttons)
        self.pb_edit_task.setObjectName(u"pb_edit_task")
        self.pb_edit_task.setMinimumSize(QSize(110, 30))
        self.pb_edit_task.setMaximumSize(QSize(140, 40))

        self.horizontalLayout_2.addWidget(self.pb_edit_task)


        self.verticalLayout_4.addWidget(self.wg_description_buttons)


        self.horizontalLayout_3.addWidget(self.wg_main_descripton)

        frm_main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(frm_main_window)
        self.statusbar.setObjectName(u"statusbar")
        frm_main_window.setStatusBar(self.statusbar)

        self.retranslateUi(frm_main_window)
        self.pb_show_description.clicked["bool"].connect(self.wg_main_descripton.setHidden)

        self.tb_tasks.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(frm_main_window)
    # setupUi

    def retranslateUi(self, frm_main_window):
        frm_main_window.setWindowTitle(QCoreApplication.translate("frm_main_window", u"Task Manager Beta", None))
        self.lb_tasks.setText(QCoreApplication.translate("frm_main_window", u"Aufgaben", None))
        self.tb_tasks.setItemText(self.tb_tasks.indexOf(self.high), QCoreApplication.translate("frm_main_window", u"Hoch", None))
        self.tb_tasks.setItemText(self.tb_tasks.indexOf(self.medium), QCoreApplication.translate("frm_main_window", u"Mittel", None))
        self.tb_tasks.setItemText(self.tb_tasks.indexOf(self.low), QCoreApplication.translate("frm_main_window", u"Niedrig", None))
        self.pb_new_task.setText(QCoreApplication.translate("frm_main_window", u"Neue Aufgabe", None))
        self.pb_show_description.setText(QCoreApplication.translate("frm_main_window", u"Detailansicht", None))
        self.lb_task_title.setText(QCoreApplication.translate("frm_main_window", u"\u00dcberschrift Aufgabe", None))
        self.pb_finish_task.setText(QCoreApplication.translate("frm_main_window", u"Abschlie\u00dfen", None))
        self.pb_edit_task.setText(QCoreApplication.translate("frm_main_window", u"Bearbeiten", None))
    # retranslateUi

