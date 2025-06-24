import sys

from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

from UI.frm_new_task import Ui_frm_new_task
from animations.button_animator import ButtonAnimator

from utils.task import Task
from utils.manage_tasks import ManageTasks

class NewTask(qtw.QWidget, Ui_frm_new_task):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.wg_time_expand.setHidden(True)
        self.ded_description.setDate(qtc.QDate.currentDate())
        self.ted_description.setTime(qtc.QTime.currentTime())

        # Animationen Buttons
        animated_buttons = ["pb_close", "pb_finish_task", "pb_create_task"]
        self.button_animator = ButtonAnimator(self, animated_buttons)

        # Verbinde Signale
        self.pb_finish_task.clicked.connect(self.finish_task)

    @qtc.Slot()
    def finish_task(self):
        self.cb_status.setCurrentIndex(3)
        self.cb_category.setCurrentIndex(2)



if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = NewTask()
    window.show()
    with open("UI/Styles/Combinear.qss", "r") as stylesheet_file:
        app.setStyleSheet(stylesheet_file.read())
    sys.exit(app.exec())