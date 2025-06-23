import sys

from PySide6 import QtWidgets as qtw

from UI.frm_new_task import Ui_frm_new_task
from animations.button_animator import ButtonAnimator

class NewTask(qtw.QWidget, Ui_frm_new_task):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Animationen
        animated_buttons = ["pb_close", "pb_finish_task", "pb_create_task"]
        self.button_animator = ButtonAnimator(self, animated_buttons)

        self.wg_time_expand.setHidden(True)


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = NewTask()
    window.show()
    with open("UI/Styles/Combinear.qss", "r") as stylesheet_file:
        app.setStyleSheet(stylesheet_file.read())
    sys.exit(app.exec())