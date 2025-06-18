# main.py
import sys

from PySide6 import QtWidgets as qtw

from UI.frm_main_window import Ui_frm_main_window
from animations.animation_handler import SidePanelAnimator
from animations.button_animator import ButtonAnimator

class MainWindow(qtw.QMainWindow, Ui_frm_main_window):

    def __init__(self):
        super().__init__()
        # setupUi() erstellt alle Widgets aus dem Designer als Attribute von 'self'
        self.setupUi(self)
        self.resize(320, 500)

        # Initialisiere den Animator, nachdem das UI aufgebaut wurde.
        self.animator = SidePanelAnimator(
            parent_window=self,  # Übergib die MainWindow-Instanz
            animated_widget_name="wg_main_description", # Name aus dem Qt Designer
            toggle_button_name="pb_show_description") # Name aus dem Qt Designer)

        # BUTTON-ANIMATIONEN
        try:
            # Liste hier alle Buttons auf, die den Effekt bekommen sollen.
            # Die Namen müssen exakt mit denen aus dem Qt Designer übereinstimmen.
            animated_buttons = [
                "pb_new_task",
                "pb_show_description", # Ja, auch der kann animiert werden!
                "pb_finish_task",
                "pb_edit_task"
            ]
            self.button_animator = ButtonAnimator(self, animated_buttons)
        except Exception as e:
            print(f"Fehler bei der Initialisierung des Button-Animators: {e}")

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # Stylesheet nach dem Anzeigen des Fensters laden, um sicherzustellen, dass es angewendet wird
    try:
        with open("UI/Styles/Combinear.qss", "r") as stylesheet_file:
            app.setStyleSheet(stylesheet_file.read())
    except FileNotFoundError:
        print("Stylesheet-Datei 'UI/Styles/Combinear.qss' nicht gefunden.")
    sys.exit(app.exec())