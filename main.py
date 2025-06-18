# main.py
import sys

from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

# UI and animation imports
from UI.frm_main_window import Ui_frm_main_window
from animations.animation_handler import SidePanelAnimator


class MainWindow(qtw.QMainWindow, Ui_frm_main_window):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        loader = qtw.QUiLoader()
        # self.ui wird das Fensterobjekt aus der .ui-Datei sein
        self.ui = loader.load("frm_main_window.ui", self)

        # Stelle sicher, dass das geladene UI-Widget das zentrale Widget des QMainWindow wird
        # Dies ist wichtig, damit das Fenster korrekt angezeigt und skaliert wird.
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Task Manager Beta")

        # --- Hier wird die Magie initialisiert! ---
        # Erstelle eine Instanz unseres Animators.
        # Übergib das Hauptfenster (self) und die Namen der Widgets aus dem Designer.
        try:
            self.side_panel_animator = SidePanelAnimator(
                parent_window=self,
                animated_widget_name="wg_main_description",
                toggle_button_name="pb_show_description"
            )
        except ValueError as e:
            print(f"Fehler bei der Initialisierung des Animators: {e}")


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    # Stylesheet nach dem Anzeigen des Fensters laden, um sicherzustellen, dass es angewendet wird
    try:
        with open("UI/Styles/Combinear.qss", "r") as stylesheet_file:
            app.setStyleSheet(stylesheet_file.read())
    except FileNotFoundError:
        print("Stylesheet-Datei nicht gefunden.")
    sys.exit(app.exec())