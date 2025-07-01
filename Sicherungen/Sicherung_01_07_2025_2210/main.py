# --- START OF FILE main.py (FINAL mit neuen Features) ---

import sys

from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
# NEU: Import für Farben
from PySide6.QtGui import QColor

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
        self.wg_description_time.setHidden(True)

        self.taskmanager = ManageTasks()
        self.taskmanager.load_from_json()

        self.animator = SidePanelAnimator(parent_window=self, animated_widget_name="wg_main_description",
                                          toggle_button_name="pb_show_description")

        animated_buttons = ["pb_new_task", "pb_show_description", "pb_finish_task", "pb_edit_task"]
        self.button_animator = ButtonAnimator(self, animated_buttons)

        self.refresh_ui()
        self.connect_signals()
        self.pb_edit_task.setDisabled(True)

    def connect_signals(self):
        self.pb_new_task.clicked.connect(self.open_new_task_window)
        self.pb_edit_task.clicked.connect(self.open_edit_task_window)
        self.lw_work.currentItemChanged.connect(self.on_item_selection_changed)
        self.lw_home.currentItemChanged.connect(self.on_item_selection_changed)
        self.lw_other.currentItemChanged.connect(self.on_item_selection_changed)
        self.lw_finished.currentItemChanged.connect(self.on_item_selection_changed)
        self.tb_tasks.currentChanged.connect(self.clear_selection)

    # GEÄNDERT: refresh_ui wurde stark erweitert
    def refresh_ui(self):
        """
        Aktualisiert die gesamte UI:
        - Zählt Aufgaben pro Kategorie und zeigt die Anzahl an.
        - Färbt überfällige Aufgaben und Kategorie-Titel rot.
        - Färbt Aufgaben nach ihrem Status.
        """
        # Speichert die aktuelle Auswahl, um sie später wiederherzustellen
        current_selection = self.get_selected_task()

        # Listen leeren
        for list_widget in [self.lw_work, self.lw_home, self.lw_other, self.lw_finished]:
            list_widget.clear()

        # Zähler und Flags für Überfälligkeit initialisieren
        counts = {"work": 0, "home": 0, "other": 0, "finished": 0}
        overdue = {"work": False, "home": False, "other": False}

        # Farbschema für den Status definieren
        status_colors = {
            "in bearbeitung": QColor("turquoise"),
            "unterbrochen": QColor("yellow"),
            "noch nicht angefangen": QColor("violet"),
            "erledigt": QColor("lightgreen")
        }
        overdue_color = QColor("red")

        # Alle Aufgaben durchgehen, sortieren und färben
        for task in self.taskmanager.task_list:
            item = qtw.QListWidgetItem(task.title)
            item.setData(qtc.Qt.UserRole, task)

            is_task_overdue = task.is_overdue()

            # Farbe basierend auf Priorität setzen: 1. Überfällig, 2. Status
            if is_task_overdue:
                item.setForeground(overdue_color)
            elif task.status.lower() in status_colors:
                item.setForeground(status_colors[task.status.lower()])

            # Aufgabe der richtigen Liste zuordnen und Zähler/Flags aktualisieren
            if task.status.lower() == "erledigt":
                self.lw_finished.addItem(item)
                counts["finished"] += 1
            elif task.category == "Arbeit":
                self.lw_work.addItem(item)
                counts["work"] += 1
                if is_task_overdue: overdue["work"] = True
            elif task.category == "zu Hause":
                self.lw_home.addItem(item)
                counts["home"] += 1
                if is_task_overdue: overdue["home"] = True
            else:  # Sonstige
                self.lw_other.addItem(item)
                counts["other"] += 1
                if is_task_overdue: overdue["other"] = True

        # Tab-Titel mit den neuen Zählern aktualisieren
        self.tb_tasks.setItemText(0, f"Arbeit ({counts['work']})")
        self.tb_tasks.setItemText(1, f"zu Hause ({counts['home']})")
        self.tb_tasks.setItemText(2, f"Sonstige ({counts['other']})")
        self.tb_tasks.setItemText(3, f"erledigte Aufgaben ({counts['finished']})")

        # Dynamische Eigenschaft für überfällige Tabs setzen
        # Die Reihenfolge der Buttons ist normalerweise konsistent mit der Tab-Reihenfolge
        tab_buttons = self.tb_tasks.findChildren(qtw.QToolButton)
        if len(tab_buttons) >= 4:
            tab_buttons[0].setProperty("overdue", overdue["work"])
            tab_buttons[1].setProperty("overdue", overdue["home"])
            tab_buttons[2].setProperty("overdue", overdue["other"])
            tab_buttons[3].setProperty("overdue", False)  # Erledigte können nicht überfällig sein

            # Qt anweisen, das Stylesheet neu auszuwerten
            for button in tab_buttons:
                self.tb_tasks.style().unpolish(button)
                self.tb_tasks.style().polish(button)

        # Auswahl wiederherstellen, falls möglich
        if not current_selection:
            self.clear_selection()
        else:
            # Manuelles Wiederherstellen ist komplex, ein einfacher Aufruf reicht oft
            self.on_item_selection_changed(self.get_selected_item())

    # HILFSFUNKTION: Gibt das ausgewählte Item-Objekt zurück
    def get_selected_item(self) -> qtw.QListWidgetItem | None:
        current_page = self.tb_tasks.currentWidget()
        if current_page:
            list_widget = current_page.findChild(qtw.QListWidget)
            if list_widget:
                return list_widget.currentItem()
        return None

    # Die folgenden Methoden bleiben größtenteils gleich,
    # werden hier aber zur Vollständigkeit aufgeführt.
    @qtc.Slot(Task)
    def add_new_task(self, task: Task):
        self.taskmanager.append_task(task)
        self.taskmanager.save_to_json()
        self.refresh_ui()

    @qtc.Slot(Task)
    def update_task_list(self, updated_task: Task):
        self.taskmanager.save_to_json()
        self.refresh_ui()

    @qtc.Slot(qtw.QListWidgetItem)
    def on_item_selection_changed(self, current_item: qtw.QListWidgetItem, previous_item: qtw.QListWidgetItem = None):
        if not current_item:
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
                    self.wg_description_time.setDisabled(True)
            else:
                self.wg_description_time.setDisabled(True)

    @qtc.Slot()
    def clear_selection(self):
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
        item = self.get_selected_item()
        return item.data(qtc.Qt.UserRole) if item else None

    @qtc.Slot()
    def open_new_task_window(self):
        if self.frm_new_task:
            self.frm_new_task.activateWindow()
            return
        self.frm_new_task = NewTask()
        self.frm_new_task.task_created.connect(self.add_new_task)
        self.frm_new_task.destroyed.connect(lambda: setattr(self, 'frm_new_task', None))
        self.frm_new_task.show()

    @qtc.Slot()
    def open_edit_task_window(self):
        selected_task = self.get_selected_task()
        if not selected_task:
            return
        if self.frm_new_task:
            self.frm_new_task.activateWindow()
            return
        self.frm_new_task = NewTask(task_to_edit=selected_task)
        self.frm_new_task.task_updated.connect(self.update_task_list)
        self.frm_new_task.task_finished.connect(self.update_task_list)
        self.frm_new_task.destroyed.connect(lambda: setattr(self, 'frm_new_task', None))
        self.frm_new_task.show()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = MainWindow()

    # NEU: Zusätzliche Stylesheet-Regel für die rote Färbung
    stylesheet = ""
    try:
        with open("UI/Styles/Adapticnew.qss", "r") as stylesheet_file:
            stylesheet = stylesheet_file.read()
    except FileNotFoundError:
        print("Stylesheet 'Adapticnew.qss' nicht gefunden. Starte mit Standard-Stil.")

    # Füge die neue Regel für überfällige Tabs hinzu
    overdue_style = """
    QToolButton[overdue="true"] {
        color: red;
        font-weight: bold;
    }
    """
    app.setStyleSheet(stylesheet + overdue_style)

    window.show()
    sys.exit(app.exec())