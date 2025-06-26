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
        frm_main_window.resize(584, 500)
        font = QFont()
        font.setFamilies([u"Calibri"])
        font.setPointSize(12)
        frm_main_window.setFont(font)
        self.centralwidget = QWidget(frm_main_window)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setMinimumSize(QSize(200, 300))
        self.horizontalLayout_3 = QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(5, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.wg_main_tasks = QWidget(self.centralwidget)
        self.wg_main_tasks.setObjectName(u"wg_main_tasks")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.wg_main_tasks.sizePolicy().hasHeightForWidth())
        self.wg_main_tasks.setSizePolicy(sizePolicy1)
        self.wg_main_tasks.setMinimumSize(QSize(270, 0))
        self.wg_main_tasks.setMaximumSize(QSize(550, 16777215))
        self.verticalLayout_5 = QVBoxLayout(self.wg_main_tasks)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(-1, 0, -1, 0)
        self.lb_tasks = QLabel(self.wg_main_tasks)
        self.lb_tasks.setObjectName(u"lb_tasks")
        font1 = QFont()
        font1.setFamilies([u"Calibri"])
        font1.setPointSize(14)
        font1.setBold(True)
        self.lb_tasks.setFont(font1)
        self.lb_tasks.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_5.addWidget(self.lb_tasks)

        self.tb_tasks = QToolBox(self.wg_main_tasks)
        self.tb_tasks.setObjectName(u"tb_tasks")
        self.work = QWidget()
        self.work.setObjectName(u"work")
        self.work.setGeometry(QRect(0, 0, 252, 238))
        self.verticalLayout = QVBoxLayout(self.work)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lw_work = QListWidget(self.work)
        self.lw_work.setObjectName(u"lw_work")
        self.lw_work.setLayoutDirection(Qt.LayoutDirection.LeftToRight)

        self.verticalLayout.addWidget(self.lw_work)

        self.tb_tasks.addItem(self.work, u"Arbeit")
        self.home = QWidget()
        self.home.setObjectName(u"home")
        self.home.setGeometry(QRect(0, 0, 252, 238))
        self.verticalLayout_2 = QVBoxLayout(self.home)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lw_home = QListWidget(self.home)
        self.lw_home.setObjectName(u"lw_home")

        self.verticalLayout_2.addWidget(self.lw_home)

        self.tb_tasks.addItem(self.home, u"zu Hause")
        self.other = QWidget()
        self.other.setObjectName(u"other")
        self.other.setGeometry(QRect(0, 0, 252, 238))
        self.verticalLayout_6 = QVBoxLayout(self.other)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.lw_other = QListWidget(self.other)
        self.lw_other.setObjectName(u"lw_other")

        self.verticalLayout_6.addWidget(self.lw_other)

        self.tb_tasks.addItem(self.other, u"Sonstige")
        self.finished_tasks = QWidget()
        self.finished_tasks.setObjectName(u"finished_tasks")
        self.finished_tasks.setGeometry(QRect(0, 0, 252, 238))
        self.verticalLayout_3 = QVBoxLayout(self.finished_tasks)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.lw_finished = QListWidget(self.finished_tasks)
        self.lw_finished.setObjectName(u"lw_finished")

        self.verticalLayout_3.addWidget(self.lw_finished)

        self.tb_tasks.addItem(self.finished_tasks, u"erledigte Aufgaben")

        self.verticalLayout_5.addWidget(self.tb_tasks)

        self.wg_tasks_buttons = QWidget(self.wg_main_tasks)
        self.wg_tasks_buttons.setObjectName(u"wg_tasks_buttons")
        self.horizontalLayout = QHBoxLayout(self.wg_tasks_buttons)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, -1, 0, -1)
        self.pb_new_task = QPushButton(self.wg_tasks_buttons)
        self.pb_new_task.setObjectName(u"pb_new_task")
        self.pb_new_task.setMinimumSize(QSize(110, 30))
        self.pb_new_task.setMaximumSize(QSize(140, 40))

        self.horizontalLayout.addWidget(self.pb_new_task)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)

        self.pb_show_description = QPushButton(self.wg_tasks_buttons)
        self.pb_show_description.setObjectName(u"pb_show_description")
        self.pb_show_description.setMinimumSize(QSize(110, 30))
        self.pb_show_description.setMaximumSize(QSize(140, 40))
        self.pb_show_description.setCheckable(True)
        self.pb_show_description.setAutoDefault(False)

        self.horizontalLayout.addWidget(self.pb_show_description)


        self.verticalLayout_5.addWidget(self.wg_tasks_buttons)


        self.horizontalLayout_3.addWidget(self.wg_main_tasks)

        self.wg_main_description = QWidget(self.centralwidget)
        self.wg_main_description.setObjectName(u"wg_main_description")
        sizePolicy1.setHeightForWidth(self.wg_main_description.sizePolicy().hasHeightForWidth())
        self.wg_main_description.setSizePolicy(sizePolicy1)
        self.wg_main_description.setMinimumSize(QSize(0, 0))
        self.wg_main_description.setMaximumSize(QSize(550, 16777215))
        self.verticalLayout_4 = QVBoxLayout(self.wg_main_description)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(-1, 0, -1, 0)
        self.lb_description = QLabel(self.wg_main_description)
        self.lb_description.setObjectName(u"lb_description")
        self.lb_description.setFont(font1)
        self.lb_description.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_4.addWidget(self.lb_description)

        self.lb_task_title = QLabel(self.wg_main_description)
        self.lb_task_title.setObjectName(u"lb_task_title")
        font2 = QFont()
        font2.setFamilies([u"Calibri"])
        font2.setPointSize(12)
        font2.setBold(True)
        self.lb_task_title.setFont(font2)
        self.lb_task_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.verticalLayout_4.addWidget(self.lb_task_title)

        self.te_description = QTextEdit(self.wg_main_description)
        self.te_description.setObjectName(u"te_description")
        self.te_description.setReadOnly(True)

        self.verticalLayout_4.addWidget(self.te_description)

        self.wg_description_time = QWidget(self.wg_main_description)
        self.wg_description_time.setObjectName(u"wg_description_time")
        self.wg_description_time.setFont(font)
        self.horizontalLayout_4 = QHBoxLayout(self.wg_description_time)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.ded_description = QDateEdit(self.wg_description_time)
        self.ded_description.setObjectName(u"ded_description")
        self.ded_description.setReadOnly(True)
        self.ded_description.setCalendarPopup(True)
        self.ded_description.setDate(QDate(2025, 6, 19))

        self.horizontalLayout_4.addWidget(self.ded_description)

        self.ted_description = QTimeEdit(self.wg_description_time)
        self.ted_description.setObjectName(u"ted_description")
        self.ted_description.setReadOnly(True)
        self.ted_description.setTime(QTime(10, 20, 0))

        self.horizontalLayout_4.addWidget(self.ted_description)


        self.verticalLayout_4.addWidget(self.wg_description_time)

        self.wg_description_buttons = QWidget(self.wg_main_description)
        self.wg_description_buttons.setObjectName(u"wg_description_buttons")
        self.horizontalLayout_2 = QHBoxLayout(self.wg_description_buttons)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, -1, 0, -1)
        self.pb_finish_task = QPushButton(self.wg_description_buttons)
        self.pb_finish_task.setObjectName(u"pb_finish_task")
        self.pb_finish_task.setMinimumSize(QSize(110, 30))
        self.pb_finish_task.setMaximumSize(QSize(140, 40))

        self.horizontalLayout_2.addWidget(self.pb_finish_task)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.pb_edit_task = QPushButton(self.wg_description_buttons)
        self.pb_edit_task.setObjectName(u"pb_edit_task")
        self.pb_edit_task.setMinimumSize(QSize(110, 30))
        self.pb_edit_task.setMaximumSize(QSize(140, 40))

        self.horizontalLayout_2.addWidget(self.pb_edit_task)


        self.verticalLayout_4.addWidget(self.wg_description_buttons)


        self.horizontalLayout_3.addWidget(self.wg_main_description)

        self.horizontalSpacer_4 = QSpacerItem(5, 20, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        frm_main_window.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(frm_main_window)
        self.statusbar.setObjectName(u"statusbar")
        frm_main_window.setStatusBar(self.statusbar)

        self.retranslateUi(frm_main_window)

        self.tb_tasks.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(frm_main_window)
    # setupUi

    def retranslateUi(self, frm_main_window):
        frm_main_window.setWindowTitle(QCoreApplication.translate("frm_main_window", u"Task Manager Beta", None))
        self.lb_tasks.setText(QCoreApplication.translate("frm_main_window", u"Aufgaben", None))
        self.tb_tasks.setItemText(self.tb_tasks.indexOf(self.work), QCoreApplication.translate("frm_main_window", u"Arbeit", None))
        self.tb_tasks.setItemText(self.tb_tasks.indexOf(self.home), QCoreApplication.translate("frm_main_window", u"zu Hause", None))
        self.tb_tasks.setItemText(self.tb_tasks.indexOf(self.other), QCoreApplication.translate("frm_main_window", u"Sonstige", None))
        self.tb_tasks.setItemText(self.tb_tasks.indexOf(self.finished_tasks), QCoreApplication.translate("frm_main_window", u"erledigte Aufgaben", None))
        self.pb_new_task.setText(QCoreApplication.translate("frm_main_window", u"Neue Aufgabe", None))
        self.pb_show_description.setText(QCoreApplication.translate("frm_main_window", u"Detailansicht", None))
        self.lb_description.setText(QCoreApplication.translate("frm_main_window", u"Beschreibung", None))
        self.lb_task_title.setText(QCoreApplication.translate("frm_main_window", u"\u00dcberschrift Aufgabe", None))
        self.pb_finish_task.setText(QCoreApplication.translate("frm_main_window", u"Abschlie\u00dfen", None))
        self.pb_edit_task.setText(QCoreApplication.translate("frm_main_window", u"Bearbeiten", None))
    # retranslateUi

