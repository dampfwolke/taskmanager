import sys

from PySide6 import QtWidgets as qtw

from UI.frm_new_task import Ui_frm_new_task

class NewTask(qtw.QWidget, Ui_frm_new_task):
    pass

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = NewTask()
    window.show()
    with open("UI/Styles/Combinear.qss", "r") as stylesheet_file:
        app.setStyleSheet(stylesheet_file.read())
    sys.exit(app.exec())