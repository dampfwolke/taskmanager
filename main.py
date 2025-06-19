import sys

from PySide6 import QtWidgets as qtw

from UI.frm_main_window import Ui_frm_main_window
from animations.animation_handler import SidePanelAnimator
from animations.button_animator import ButtonAnimator

class MainWindow(qtw.QMainWindow, Ui_frm_main_window):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.resize(360, 500)
        # Initialisiere den Animator, nachdem das UI aufgebaut wurde.
        self.animator = SidePanelAnimator(parent_window=self, animated_widget_name="wg_main_description", toggle_button_name="pb_show_description")
        # BUTTON-ANIMATIONENListe hier alle Buttons auf, die den Effekt bekommen sollen.
        animated_buttons = ["pb_new_task", "pb_show_description", "pb_finish_task", "pb_edit_task"]
        self.button_animator = ButtonAnimator(self, animated_buttons)
        

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # with open("UI/Styles/Combinear.qss", "r") as stylesheet_file:
    #     app.setStyleSheet(stylesheet_file.read())
    sys.exit(app.exec())