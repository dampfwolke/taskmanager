# main.py
import sys

from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

from UI.frm_main_window import Ui_frm_main_window
from animations.animation_handler import SidePanelAnimator


class MainWindow(qtw.QMainWindow, Ui_frm_main_window):

    def __init__(self):
        super().__init__()
        # setupUi() erstellt alle Widgets aus dem Designer als Attribute von 'self'
        self.setupUi(self)
        # self.setMaximumWidth(350)

        # --- HIER KOMMT DIE ANIMATION HINZU ---
        # Initialisiere den Animator, nachdem das UI aufgebaut wurde.
        try:
            self.animator = SidePanelAnimator(
                parent_window=self,  # Übergib die MainWindow-Instanz
                animated_widget_name="wg_main_description", # Name aus dem Qt Designer
                toggle_button_name="pb_show_description" # Name aus dem Qt Designer
            )
        except ValueError as e:
            print(f"Fehler bei der Initialisierung des Animators: {e}")
        except AttributeError:
             print("Fehler: Ein Widget-Name ist falsch oder existiert nicht. Überprüfe die Namen im Qt Designer.")


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