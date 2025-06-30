# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'frm_new_task.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateEdit,
    QFontComboBox, QFormLayout, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QTextEdit, QTimeEdit, QVBoxLayout,
    QWidget)

class Ui_frm_new_task(object):
    def setupUi(self, frm_new_task):
        if not frm_new_task.objectName():
            frm_new_task.setObjectName(u"frm_new_task")
        frm_new_task.resize(470, 689)
        self.verticalLayout_3 = QVBoxLayout(frm_new_task)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.wg_main_new_task = QWidget(frm_new_task)
        self.wg_main_new_task.setObjectName(u"wg_main_new_task")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.wg_main_new_task.sizePolicy().hasHeightForWidth())
        self.wg_main_new_task.setSizePolicy(sizePolicy)
        self.wg_main_new_task.setMinimumSize(QSize(0, 0))
        self.wg_main_new_task.setMaximumSize(QSize(550, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.wg_main_new_task)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lb_new_task = QLabel(self.wg_main_new_task)
        self.lb_new_task.setObjectName(u"lb_new_task")
        font = QFont()
        font.setFamilies([u"Calibri"])
        font.setPointSize(14)
        font.setBold(True)
        self.lb_new_task.setFont(font)
        self.lb_new_task.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.verticalLayout_2.addWidget(self.lb_new_task)

        self.wg_title = QWidget(self.wg_main_new_task)
        self.wg_title.setObjectName(u"wg_title")
        font1 = QFont()
        font1.setFamilies([u"Calibri"])
        font1.setPointSize(12)
        self.wg_title.setFont(font1)
        self.formLayout = QFormLayout(self.wg_title)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(33)
        self.formLayout.setVerticalSpacing(2)
        self.formLayout.setContentsMargins(2, 2, -1, 2)
        self.lb_title = QLabel(self.wg_title)
        self.lb_title.setObjectName(u"lb_title")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.lb_title)

        self.le_title = QLineEdit(self.wg_title)
        self.le_title.setObjectName(u"le_title")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.le_title)


        self.verticalLayout_2.addWidget(self.wg_title)

        self.wg_category = QWidget(self.wg_main_new_task)
        self.wg_category.setObjectName(u"wg_category")
        self.wg_category.setFont(font1)
        self.horizontalLayout = QHBoxLayout(self.wg_category)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, 2, -1, 2)
        self.lb_category = QLabel(self.wg_category)
        self.lb_category.setObjectName(u"lb_category")

        self.horizontalLayout.addWidget(self.lb_category)

        self.cb_category = QComboBox(self.wg_category)
        self.cb_category.addItem("")
        self.cb_category.addItem("")
        self.cb_category.addItem("")
        self.cb_category.setObjectName(u"cb_category")
        self.cb_category.setMinimumSize(QSize(200, 0))

        self.horizontalLayout.addWidget(self.cb_category)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)


        self.verticalLayout_2.addWidget(self.wg_category)

        self.wg_status = QWidget(self.wg_main_new_task)
        self.wg_status.setObjectName(u"wg_status")
        self.wg_status.setFont(font1)
        self.horizontalLayout_3 = QHBoxLayout(self.wg_status)
        self.horizontalLayout_3.setSpacing(33)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(2, 2, -1, 2)
        self.lb_status = QLabel(self.wg_status)
        self.lb_status.setObjectName(u"lb_status")

        self.horizontalLayout_3.addWidget(self.lb_status)

        self.cb_status = QComboBox(self.wg_status)
        self.cb_status.addItem("")
        self.cb_status.addItem("")
        self.cb_status.addItem("")
        self.cb_status.addItem("")
        self.cb_status.setObjectName(u"cb_status")
        self.cb_status.setMinimumSize(QSize(200, 0))

        self.horizontalLayout_3.addWidget(self.cb_status)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)


        self.verticalLayout_2.addWidget(self.wg_status)

        self.fr_description = QFrame(self.wg_main_new_task)
        self.fr_description.setObjectName(u"fr_description")
        self.fr_description.setFont(font1)
        self.fr_description.setFrameShape(QFrame.Shape.StyledPanel)
        self.fr_description.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout = QVBoxLayout(self.fr_description)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lb_description = QLabel(self.fr_description)
        self.lb_description.setObjectName(u"lb_description")
        font2 = QFont()
        font2.setFamilies([u"Calibri"])
        font2.setPointSize(12)
        font2.setBold(True)
        self.lb_description.setFont(font2)

        self.verticalLayout.addWidget(self.lb_description)

        self.te_description = QTextEdit(self.fr_description)
        self.te_description.setObjectName(u"te_description")
        self.te_description.setReadOnly(False)

        self.verticalLayout.addWidget(self.te_description)

        self.fcb_description = QFontComboBox(self.fr_description)
        self.fcb_description.setObjectName(u"fcb_description")

        self.verticalLayout.addWidget(self.fcb_description)


        self.verticalLayout_2.addWidget(self.fr_description)

        self.wg_time = QWidget(self.wg_main_new_task)
        self.wg_time.setObjectName(u"wg_time")
        self.wg_time.setFont(font1)
        self.horizontalLayout_5 = QHBoxLayout(self.wg_time)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.cbx_show_timeedit = QCheckBox(self.wg_time)
        self.cbx_show_timeedit.setObjectName(u"cbx_show_timeedit")
        self.cbx_show_timeedit.setChecked(False)

        self.horizontalLayout_5.addWidget(self.cbx_show_timeedit)


        self.verticalLayout_2.addWidget(self.wg_time)

        self.wg_time_expand = QWidget(self.wg_main_new_task)
        self.wg_time_expand.setObjectName(u"wg_time_expand")
        self.wg_time_expand.setFont(font1)
        self.horizontalLayout_4 = QHBoxLayout(self.wg_time_expand)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.ded_description = QDateEdit(self.wg_time_expand)
        self.ded_description.setObjectName(u"ded_description")
        self.ded_description.setReadOnly(False)
        self.ded_description.setCalendarPopup(True)
        self.ded_description.setDate(QDate(2025, 6, 19))

        self.horizontalLayout_4.addWidget(self.ded_description)

        self.ted_description = QTimeEdit(self.wg_time_expand)
        self.ted_description.setObjectName(u"ted_description")
        self.ted_description.setReadOnly(False)
        self.ted_description.setCalendarPopup(True)
        self.ted_description.setCurrentSectionIndex(0)
        self.ted_description.setTime(QTime(10, 20, 0))

        self.horizontalLayout_4.addWidget(self.ted_description)


        self.verticalLayout_2.addWidget(self.wg_time_expand)

        self.wg_new_task_buttons = QWidget(self.wg_main_new_task)
        self.wg_new_task_buttons.setObjectName(u"wg_new_task_buttons")
        self.wg_new_task_buttons.setFont(font1)
        self.horizontalLayout_2 = QHBoxLayout(self.wg_new_task_buttons)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, -1, 0, -1)
        self.pb_close = QPushButton(self.wg_new_task_buttons)
        self.pb_close.setObjectName(u"pb_close")
        self.pb_close.setMinimumSize(QSize(110, 30))
        self.pb_close.setMaximumSize(QSize(140, 40))

        self.horizontalLayout_2.addWidget(self.pb_close)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pb_finish_task = QPushButton(self.wg_new_task_buttons)
        self.pb_finish_task.setObjectName(u"pb_finish_task")
        self.pb_finish_task.setMinimumSize(QSize(110, 30))
        self.pb_finish_task.setMaximumSize(QSize(140, 40))

        self.horizontalLayout_2.addWidget(self.pb_finish_task)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.pb_create_task = QPushButton(self.wg_new_task_buttons)
        self.pb_create_task.setObjectName(u"pb_create_task")
        self.pb_create_task.setMinimumSize(QSize(110, 30))
        self.pb_create_task.setMaximumSize(QSize(140, 40))

        self.horizontalLayout_2.addWidget(self.pb_create_task)


        self.verticalLayout_2.addWidget(self.wg_new_task_buttons)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)


        self.verticalLayout_3.addWidget(self.wg_main_new_task)


        self.retranslateUi(frm_new_task)
        self.pb_close.clicked.connect(frm_new_task.close)
        self.cbx_show_timeedit.clicked["bool"].connect(self.wg_time_expand.setVisible)
        self.fcb_description.currentFontChanged.connect(self.te_description.setCurrentFont)

        QMetaObject.connectSlotsByName(frm_new_task)
    # setupUi

    def retranslateUi(self, frm_new_task):
        frm_new_task.setWindowTitle(QCoreApplication.translate("frm_new_task", u"Neue Aufgabe erstellen", None))
        self.lb_new_task.setText(QCoreApplication.translate("frm_new_task", u"Neue Aufgabe erstellen", None))
        self.lb_title.setText(QCoreApplication.translate("frm_new_task", u"Name:", None))
        self.lb_category.setText(QCoreApplication.translate("frm_new_task", u"Kategorie:", None))
        self.cb_category.setItemText(0, QCoreApplication.translate("frm_new_task", u"Arbeit", None))
        self.cb_category.setItemText(1, QCoreApplication.translate("frm_new_task", u"zu Hause", None))
        self.cb_category.setItemText(2, QCoreApplication.translate("frm_new_task", u"erledigte Aufgaben", None))

        self.lb_status.setText(QCoreApplication.translate("frm_new_task", u"Status:", None))
        self.cb_status.setItemText(0, QCoreApplication.translate("frm_new_task", u"in Bearbeitung", None))
        self.cb_status.setItemText(1, QCoreApplication.translate("frm_new_task", u"unterbrochen", None))
        self.cb_status.setItemText(2, QCoreApplication.translate("frm_new_task", u"noch nicht angefangen", None))
        self.cb_status.setItemText(3, QCoreApplication.translate("frm_new_task", u"Erledigt", None))

        self.lb_description.setText(QCoreApplication.translate("frm_new_task", u"Beschreibung der Aufgabe:", None))
        self.cbx_show_timeedit.setText(QCoreApplication.translate("frm_new_task", u"Termin festlegen", None))
        self.pb_close.setText(QCoreApplication.translate("frm_new_task", u"Beenden", None))
        self.pb_finish_task.setText(QCoreApplication.translate("frm_new_task", u"Abschlie\u00dfen", None))
        self.pb_create_task.setText(QCoreApplication.translate("frm_new_task", u"Erstellen", None))
    # retranslateUi

