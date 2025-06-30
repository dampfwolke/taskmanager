# --- START OF FILE main.py (FINAL) ---

import sys

from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc

from UI.frm_main_window import Ui_frm_main_window
from animations.animation_handler import SidePanelAnimator
from animations.button_animator import ButtonAnimator

from new_task import NewTask
from utils.manage_tasks import ManageTasks
from utils.task import Task


class MainWindow(qtw.QMainWindow, Ui_frm_main_window):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.frm_new_task = None
        self.resize(360, 500)
        self.lb_task_title.setText("")
        self.te_description.clear()

        # ManageTasks Klasse aufrufen
        self.taskmanager = ManageTasks()
        self.taskmanager.load_from_json()

        # 1. Animatoren zuerst initialisieren, damit sie existieren
        self.animator = SidePanelAnimator(parent_window=self, animated_widget_name="wg_main_description",
                                          toggle_button_name="pb_show_description")

        animated_buttons = ["pb_new_task", "pb_show_description", "pb_finish_task", "pb_edit_task"]
        self.button_animator = ButtonAnimator(self, animated_buttons)

        # 2. UI aktualisieren (diese Methode kann den Animator jetzt sicher aufrufen)
        self.refresh_ui()

        # 3. Signale verbinden
        self.connect_signals()

        # 4. Zusätzliche UI-Anpassungen beim Start
        self.pb_edit_task.setDisabled(True)

    def connect_signals(self):
        """Sammelt alle Signal-Slot-Verbindungen an einem Ort."""
        # GEÄNDERT: Verbindet mit den neuen, klarer benannten Methoden
        self.pb_new_task.clicked.connect(self.open_new_task_window)
        self.pb_edit_task.clicked.connect(self.open_edit_task_window)

        # Detail-Button wird vom Animator gesteuert. Hier ist kein direkter Slot mehr nötig.

        # Verbindet die Auswahländerung in den Listen mit dem entsprechenden Slot
        self.lw_work.currentItemChanged.connect(self.on_item_selection_changed)
        self.lw_home.currentItemChanged.connect(self.on_item_selection_changed)
        self.lw_other.currentItemChanged.connect(self.on_item_selection_changed)
        self.lw_finished.currentItemChanged.connect(self.on_item_selection_changed)

        # Hebt die Auswahl auf, wenn der Tab gewechselt wird
        self.tb_tasks.currentChanged.connect(self.clear_selection)

    def refresh_ui(self):
        """Löscht alle Listen und füllt sie basierend auf der Task-Liste neu."""
        current_selection = self.get_selected_task()

        self.lw_work.clear()
        self.lw_home.clear()
        self.lw_other.clear()
        self.lw_finished.clear()

        new_item_to_select = None

        for task in self.taskmanager.task_list:
            item = qtw.QListWidgetItem(task.title)
            item.setData(qtc.Qt.UserRole, task)

            # Auswahl nach dem Refresh wiederherstellen
            if current_selection and task is current_selection:
                new_item_to_select = item

            if task.status.lower() == "erledigt":
                self.lw_finished.addItem(item)
                if new_item_to_select and new_item_to_select is item:
                    self.lw_finished.setCurrentItem(item)
            elif task.category == "zu Hause":
                self.lw_home.addItem(item)
                if new_item_to_select and new_item_to_select is item:
                    self.lw_home.setCurrentItem(item)
            elif task.category == "Arbeit":
                self.lw_work.addItem(item)
                if new_item_to_select and new_item_to_select is item:
                    self.lw_work.setCurrentItem(item)
            else:
                self.lw_other.addItem(item)
                if new_item_to_select and new_item_to_select is item:
                    self.lw_other.setCurrentItem(item)

        if not new_item_to_select:
            self.clear_selection()

    @qtc.Slot(Task)
    def add_new_task(self, task: Task):
        """Fügt eine neue Aufgabe hinzu, speichert und aktualisiert die UI."""
        self.taskmanager.append_task(task)
        self.taskmanager.save_to_json()
        self.refresh_ui()
        print(f"Neue Aufgabe '{task.title}' hinzugefügt.")

    @qtc.Slot(Task)
    def update_task_list(self, updated_task: Task):
        """Slot, der auf Änderungen reagiert (Speichern oder Abschließen)."""
        # Da wir mit Objekten arbeiten, ist die Liste bereits aktuell.
        # Wir müssen nur speichern und die UI neu zeichnen.
        self.taskmanager.save_to_json()
        self.refresh_ui()
        print(f"Aufgabe '{updated_task.title}' aktualisiert.")

    @qtc.Slot(qtw.QListWidgetItem)
    def on_item_selection_changed(self, current_item: qtw.QListWidgetItem, previous_item: qtw.QListWidgetItem = None):
        """Wird aufgerufen, wenn ein Item in einer der Listen ausgewählt wird."""
        if current_item is None:
            self.pb_edit_task.setDisabled(True)
            self.pb_show_description.setDisabled(True)
            return

        task = current_item.data(qtc.Qt.UserRole)

        if task:
            self.pb_show_description.setDisabled(False)
            self.pb_edit_task.setDisabled(False)
            self.lb_task_title.setText(task.title)
            self.te_description.setText(task.description)

            if task.due_date:
                try:
                    due_datetime = qtc.QDateTime.fromString(task.due_date, "yyyy-MM-dd HH:mm:ss")
                    self.ded_description.setDate(due_datetime.date())
                    self.ted_description.setTime(due_datetime.time())
                    self.wg_description_time.setDisabled(False)
                except Exception as e:
                    print(f"Fehler beim Parsen des Datums: {e}")
                    self.wg_description_time.setDisabled(True)
            else:
                self.wg_description_time.setDisabled(True)

    @qtc.Slot()
    def clear_selection(self):
        """Hebt die Auswahl in allen Listen auf und leert die Detailansicht."""
        for list_widget in [self.lw_work, self.lw_home, self.lw_other, self.lw_finished]:
            list_widget.setCurrentItem(None)

        self.lb_task_title.setText("")
        self.te_description.clear()
        self.wg_description_time.setDisabled(True)
        self.pb_show_description.setDisabled(True)
        self.pb_show_description.setChecked(False)
        self.pb_edit_task.setDisabled(True)
        self.animator.hide_panel()

    def get_selected_task(self) -> Task | None:
        """Hilfsfunktion, um die aktuell ausgewählte Aufgabe zu finden."""
        # Das aktuelle Widget im ToolBox finden
        current_page = self.tb_tasks.currentWidget()
        # Darin das QListWidget finden
        current_list_widget = current_page.findChild(qtw.QListWidget)

        if current_list_widget:
            current_item = current_list_widget.currentItem()
            if current_item:
                return current_item.data(qtc.Qt.UserRole)
        return None

    @qtc.Slot()
    def open_new_task_window(self):
        """Öffnet das Fenster zum Erstellen einer neuen Aufgabe (CREATE-Modus)."""
        if self.frm_new_task:
            self.frm_new_task.activateWindow()
            return

        self.frm_new_task = NewTask(parent=self)  # parent=self ist gut für Dialoge
        self.frm_new_task.task_created.connect(self.add_new_task)
        # finished-Signal existiert jetzt und funktioniert wie erwartet
        self.frm_new_task.finished.connect(lambda: setattr(self, 'frm_new_task', None))
        # .open() ist der nicht-blockierende Weg, einen Dialog zu zeigen
        self.frm_new_task.open()

    @qtc.Slot()
    def open_edit_task_window(self):
        """Öffnet das Fenster zum Bearbeiten der ausgewählten Aufgabe (EDIT-Modus)."""
        selected_task = self.get_selected_task()
        if not selected_task:
            qtw.QMessageBox.information(self, "Keine Auswahl", "Bitte wählen Sie zuerst eine Aufgabe zum Bearbeiten aus.")
            return

        if self.frm_new_task:
            self.frm_new_task.activateWindow()
            return

        self.frm_new_task = NewTask(task_to_edit=selected_task, parent=self)
        self.frm_new_task.task_updated.connect(self.update_task_list)
        self.frm_new_task.task_finished.connect(self.update_task_list)
        self.frm_new_task.finished.connect(lambda: setattr(self, 'frm_new_task', None))
        # .open() statt .show()
        self.frm_new_task.open()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    try:
        with open("UI/Styles/Adapticnew.qss", "r") as stylesheet_file:
            app.setStyleSheet(stylesheet_file.read())
    except FileNotFoundError:
        print("Stylesheet 'Adapticnew.qss' nicht gefunden. Starte mit Standard-Stil.")
    sys.exit(app.exec())