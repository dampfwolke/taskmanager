# --- START OF FILE new_task.py (ÜBERARBEITET) ---

import sys
from enum import Enum, auto

from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

from UI.frm_new_task import Ui_frm_new_task
from animations.button_animator import ButtonAnimator
from utils.task import Task


# NEU: Modi definieren, um den Code lesbarer zu machen
class WindowMode(Enum):
    CREATE = auto()
    EDIT = auto()


class NewTask(qtw.QDialog, Ui_frm_new_task):
    # Bestehendes Signal für neue Aufgaben
    task_created = qtc.Signal(Task)
    # NEU: Signal für aktualisierte Aufgaben
    task_updated = qtc.Signal(Task)
    # NEU: Signal, um eine Aufgabe als erledigt zu markieren
    task_finished = qtc.Signal(Task)

    # GEÄNDERT: Konstruktor akzeptiert jetzt eine optionale Aufgabe
    def __init__(self, task_to_edit: Task = None, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # Das zu bearbeitende Task-Objekt speichern
        self.current_task = task_to_edit

        # Den Modus basierend auf der Übergabe festlegen
        self.mode = WindowMode.EDIT if self.current_task else WindowMode.CREATE

        # UI für den entsprechenden Modus einrichten
        self._setup_ui_for_mode()

        # Animationen für die Buttons
        self._setup_animations()

        # Signale verbinden
        self._connect_signals()

    def _setup_ui_for_mode(self):
        """Passt die Benutzeroberfläche je nach Modus (Erstellen oder Bearbeiten) an."""

        # Befüllen der ComboBoxen (besser hier als im Designer für Flexibilität)
        self.cb_category.clear()
        self.cb_category.addItems(["Arbeit", "zu Hause", "Sonstige"])
        self.cb_status.clear()
        self.cb_status.addItems(["in Bearbeitung", "unterbrochen", "noch nicht angefangen"])

        if self.mode == WindowMode.CREATE:
            # --- Modus: NEUE AUFGABE ERSTELLEN ---
            self.setWindowTitle("Neue Aufgabe erstellen")
            self.lb_new_task.setText("Neue Aufgabe erstellen")
            self.pb_create_task.setText("Erstellen")

            # Button zum Abschließen ist bei neuen Aufgaben nicht sichtbar
            self.pb_finish_task.setHidden(True)

            # Zeit/Datum Felder standardmäßig ausblenden und auf heute setzen
            self.wg_time_expand.setHidden(True)
            self.cbx_show_timeedit.setChecked(False)
            self.ded_description.setDate(qtc.QDate.currentDate())
            self.ted_description.setTime(qtc.QTime.currentTime())

        else:  # self.mode == WindowMode.EDIT
            # --- Modus: AUFGABE BEARBEITEN ---
            self.setWindowTitle("Aufgabe bearbeiten")
            self.lb_new_task.setText("Aufgabe bearbeiten")
            self.pb_create_task.setText("Speichern")

            # Button zum Abschließen sichtbar machen
            self.pb_finish_task.setHidden(False)

            # Formularfelder mit den Daten der Aufgabe befüllen
            self.populate_fields()

    def populate_fields(self):
        """Befüllt die UI-Felder mit den Daten von self.current_task."""
        if not self.current_task:
            return

        self.le_title.setText(self.current_task.title)
        self.te_description.setPlainText(self.current_task.description)
        self.cb_category.setCurrentText(self.current_task.category)
        self.cb_status.setCurrentText(self.current_task.status)

        if self.current_task.due_date:
            self.wg_time_expand.setHidden(False)
            self.cbx_show_timeedit.setChecked(True)
            due_datetime = qtc.QDateTime.fromString(self.current_task.due_date, "yyyy-MM-dd HH:mm:ss")
            self.ded_description.setDateTime(due_datetime)
            self.ted_description.setDateTime(due_datetime)
        else:
            self.wg_time_expand.setHidden(True)
            self.cbx_show_timeedit.setChecked(False)
            self.ded_description.setDate(qtc.QDate.currentDate())
            self.ted_description.setTime(qtc.QTime.currentTime())

    def _setup_animations(self):
        """Initialisiert die Button-Animationen."""
        animated_buttons = ["pb_close", "pb_finish_task", "pb_create_task"]
        self.button_animator = ButtonAnimator(self, animated_buttons)

    def _connect_signals(self):
        """Verbindet die Signale der UI-Elemente mit den Slots."""
        # Der Haupt-Button ruft je nach Modus eine andere Aktion auf
        self.pb_create_task.clicked.connect(self.save_or_create_task)
        # Der Abschließen-Button hat eine eigene Funktion
        self.pb_finish_task.clicked.connect(self.finish_task)

    @qtc.Slot()
    def save_or_create_task(self):
        """Wrapper-Funktion, die entscheidet, ob gespeichert oder neu erstellt wird."""
        title = self.le_title.text().strip()
        if not title:
            qtw.QMessageBox.warning(self, "Fehlende Eingabe", "Bitte geben Sie einen Titel für die Aufgabe ein.")
            return

        if self.mode == WindowMode.CREATE:
            # --- Neue Aufgabe erstellen ---
            new_task = Task(
                title=title,
                description=self.te_description.toPlainText(),
                category=self.cb_category.currentText(),
                status=self.cb_status.currentText(),
                due_date=self._get_due_date_string()
            )
            self.task_created.emit(new_task)

        else:  # self.mode == WindowMode.EDIT
            # --- Bestehende Aufgabe aktualisieren ---
            self.current_task.title = title
            self.current_task.description = self.te_description.toPlainText()
            self.current_task.category = self.cb_category.currentText()
            self.current_task.status = self.cb_status.currentText()
            self.current_task.due_date = self._get_due_date_string()
            self.task_updated.emit(self.current_task)

        self.close()

    @qtc.Slot()
    def finish_task(self):
        """Markiert die aktuelle Aufgabe als 'Erledigt' und sendet ein Signal."""
        if self.current_task:
            self.current_task.update_status("Erledigt")
            self.task_finished.emit(self.current_task)
            self.close()

    def _get_due_date_string(self) -> str | None:
        """Liest Datum und Zeit aus, wenn die Checkbox aktiv ist."""
        if self.cbx_show_timeedit.isChecked():
            date = self.ded_description.date().toString("yyyy-MM-dd")
            time = self.ted_description.time().toString("HH:mm:ss")
            return f"{date} {time}"
        return None


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)

    # Zum Testen des EDIT-Modus
    # test_task = Task("Test Aufgabe", "Dies ist eine Beschreibung", "Arbeit", due_date="2024-10-29 15:00:00")
    # window = NewTask(task_to_edit=test_task)

    # Zum Testen des CREATE-Modus
    window = NewTask()

    window.show()
    try:
        with open("UI/Styles/Combinear.qss", "r") as stylesheet_file:
            app.setStyleSheet(stylesheet_file.read())
    except FileNotFoundError:
        print("Stylesheet 'Combinear.qss' nicht gefunden.")
    sys.exit(app.exec())