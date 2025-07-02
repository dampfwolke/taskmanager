# --- START OF FILE main.py (FINAL mit allen neuen Features) ---

import sys

from PySide6 import QtWidgets as qtw
from PySide6 import QtCore as qtc
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

        self.taskmanager = ManageTasks()
        self.taskmanager.load_from_json()

        self.animator = SidePanelAnimator(parent_window=self, animated_widget_name="wg_main_description",
                                          toggle_button_name="pb_show_description")

        animated_buttons = ["pb_show_description", "pb_finish_task", "pb_edit_task"]
        self.button_animator = ButtonAnimator(self, animated_buttons)

        # NEU: Timer für regelmäßige UI-Updates initialisieren
        self.update_timer = qtc.QTimer(self)
        self.update_timer.setInterval(30000)  # 30 Sekunden
        self.update_timer.timeout.connect(self.refresh_ui)
        self.update_timer.start()

        self.refresh_ui()
        self.connect_signals()

        # Startzustand der Buttons setzen
        self.pb_edit_task.setDisabled(True)
        self.pb_finish_task.setDisabled(True)

    def connect_signals(self):
        self.pb_new_task.clicked.connect(self.open_new_task_window)
        self.pb_edit_task.clicked.connect(self.open_edit_task_window)

        # NEU: Button zum Abschließen verbinden
        self.pb_finish_task.clicked.connect(self.finish_selected_task)

        # Alle Listenwidgets verbinden
        for list_widget in [self.lw_work, self.lw_home, self.lw_other, self.lw_finished]:
            list_widget.currentItemChanged.connect(self.on_item_selection_changed)
            # NEU: Doppelklick-Signal verbinden
            list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)

        self.tb_tasks.currentChanged.connect(self.clear_selection)

    def refresh_ui(self):
        """
        Aktualisiert die gesamte UI: Zählt, sortiert und färbt Aufgaben.
        """
        current_selection = self.get_selected_task()

        for list_widget in [self.lw_work, self.lw_home, self.lw_other, self.lw_finished]:
            list_widget.clear()

        # Temporäre Listen für jede Kategorie, um die Sortierung vorzubereiten
        tasks_by_category = {
            "work": [], "home": [], "other": [], "finished": []
        }

        # NEU: Sortierreihenfolge definieren
        status_sort_order = {
            "überfällig": 0,
            "in bearbeitung": 1,
            "unterbrochen": 2,
            "noch nicht angefangen": 3,
            "erledigt": 4
        }
        status_colors = {
            "in bearbeitung": QColor("turquoise"),
            "unterbrochen": QColor("yellow"),
            "noch nicht angefangen": QColor("violet"),
            "erledigt": QColor("lightgreen")
        }
        overdue_color = QColor("red")

        # 1. Aufgaben sammeln und sortierbare Tupel erstellen
        for task in self.taskmanager.task_list:
            sort_key = status_sort_order.get(task.status.lower(), 99)
            if task.is_overdue():
                sort_key = status_sort_order["überfällig"]

            task_tuple = (sort_key, task)

            if task.status.lower() == "erledigt":
                tasks_by_category["finished"].append(task_tuple)
            elif task.category == "Arbeit":
                tasks_by_category["work"].append(task_tuple)
            elif task.category == "zu Hause":
                tasks_by_category["home"].append(task_tuple)
            else:
                tasks_by_category["other"].append(task_tuple)

        # 2. Aufgaben in jeder Kategorie sortieren
        for category in tasks_by_category:
            tasks_by_category[category].sort(key=lambda x: x[0])

        # 3. UI befüllen und Zähler/Flags setzen
        counts = {"work": 0, "home": 0, "other": 0, "finished": 0}
        overdue = {"work": False, "home": False, "other": False}

        # Funktion, um die UI zu füllen
        def populate_list(list_widget, category):
            for sort_key, task in tasks_by_category[category]:
                item = qtw.QListWidgetItem(task.title)
                item.setData(qtc.Qt.UserRole, task)

                is_task_overdue = (sort_key == status_sort_order["überfällig"])
                if is_task_overdue:
                    item.setForeground(overdue_color)
                    overdue[category] = True
                elif task.status.lower() in status_colors:
                    item.setForeground(status_colors[task.status.lower()])

                list_widget.addItem(item)
                counts[category] += 1

                # Auswahl wiederherstellen
                if current_selection and task is current_selection:
                    list_widget.setCurrentItem(item)

        populate_list(self.lw_work, "work")
        populate_list(self.lw_home, "home")
        populate_list(self.lw_other, "other")
        populate_list(self.lw_finished, "finished")

        # Tab-Titel und Farben aktualisieren
        self.tb_tasks.setItemText(0, f"Arbeit ({counts['work']})")
        self.tb_tasks.setItemText(1, f"zu Hause ({counts['home']})")
        self.tb_tasks.setItemText(2, f"Sonstige ({counts['other']})")
        self.tb_tasks.setItemText(3, f"erledigte Aufgaben ({counts['finished']})")

        tab_buttons = self.tb_tasks.findChildren(qtw.QToolButton)
        if len(tab_buttons) >= 4:
            tab_buttons[0].setProperty("overdue", overdue["work"])
            tab_buttons[1].setProperty("overdue", overdue["home"])
            tab_buttons[2].setProperty("overdue", overdue["other"])
            for button in tab_buttons:
                self.tb_tasks.style().unpolish(button)
                self.tb_tasks.style().polish(button)

        if not self.get_selected_item():
            self.clear_selection()

    @qtc.Slot(qtw.QListWidgetItem)
    def on_item_selection_changed(self, current_item: qtw.QListWidgetItem, previous_item: qtw.QListWidgetItem = None):
        if not current_item:
            for btn in [self.pb_edit_task, self.pb_show_description, self.pb_finish_task]:
                btn.setDisabled(True)
            return

        task = current_item.data(qtc.Qt.UserRole)
        if task:
            for btn in [self.pb_edit_task, self.pb_show_description, self.pb_finish_task]:
                btn.setDisabled(False)
            self.lb_task_title.setText(task.title)
            self.te_description.setText(task.description)

            # GEÄNDERT: `setHidden` statt `setDisabled`
            if task.due_date:
                try:
                    due_datetime = qtc.QDateTime.fromString(task.due_date, "yyyy-MM-dd HH:mm:ss")
                    self.ded_description.setDate(due_datetime.date())
                    self.ted_description.setTime(due_datetime.time())
                    self.wg_description_time.setHidden(False)
                except Exception:
                    self.wg_description_time.setHidden(True)
            else:
                self.wg_description_time.setHidden(True)

    @qtc.Slot(qtw.QListWidgetItem)
    def on_item_double_clicked(self, item: qtw.QListWidgetItem):
        """Öffnet/Schließt die Detailansicht bei Doppelklick."""
        self.animator.toggle_animation()

    @qtc.Slot()
    def finish_selected_task(self):
        """Markiert die aktuell ausgewählte Aufgabe als 'Erledigt'."""
        task_to_finish = self.get_selected_task()
        if task_to_finish:
            task_to_finish.update_status("Erledigt")
            self.update_task_list(task_to_finish)
            print(f"Aufgabe '{task_to_finish.title}' wurde abgeschlossen.")

    @qtc.Slot()
    def clear_selection(self):
        for list_widget in [self.lw_work, self.lw_home, self.lw_other, self.lw_finished]:
            list_widget.setCurrentItem(None)
        self.lb_task_title.setText("")
        self.te_description.clear()
        self.wg_description_time.setHidden(True)
        for btn in [self.pb_show_description, self.pb_edit_task, self.pb_finish_task]:
            btn.setDisabled(True)
        self.pb_show_description.setChecked(False)
        self.animator.hide_panel()

    # --- Die restlichen Methoden (add_new_task, update_task_list, etc.) bleiben wie zuvor ---

    def get_selected_item(self) -> qtw.QListWidgetItem | None:
        current_page = self.tb_tasks.currentWidget()
        if current_page:
            list_widget = current_page.findChild(qtw.QListWidget)
            if list_widget:
                return list_widget.currentItem()
        return None

    def get_selected_task(self) -> Task | None:
        item = self.get_selected_item()
        return item.data(qtc.Qt.UserRole) if item else None

    @qtc.Slot(Task)
    def add_new_task(self, task: Task):
        self.taskmanager.append_task(task)
        self.taskmanager.save_to_json()
        self.refresh_ui()

    @qtc.Slot(Task)
    def update_task_list(self, updated_task: Task):
        self.taskmanager.save_to_json()
        self.refresh_ui()

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
        if not selected_task: return
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

    stylesheet = ""
    try:
        with open("UI/Styles/Adapticnew.qss", "r") as stylesheet_file:
            stylesheet = stylesheet_file.read()
    except FileNotFoundError:
        print("Stylesheet 'Adapticnew.qss' nicht gefunden. Starte mit Standard-Stil.")

    overdue_style = """
    QToolButton[overdue="true"] {
        color: red;
        font-weight: bold;
    }
    """
    app.setStyleSheet(stylesheet + overdue_style)

    window.show()
    sys.exit(app.exec())